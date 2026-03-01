import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt

# import seaborn as sns
import os
import sys
import requests
import torch
from torch import nn, distributions
from scipy.spatial.distance import cdist
from scipy.stats import norm, multivariate_normal
import GPyOpt
import math
import rasterio
from rasterio.warp import transform


def plot_simple_regret2(all_results, peak_name):
    """Plot simple regret curves for all kernels on a given peak"""
    plt.figure(figsize=(10, 6))

    for kernel_name, trials in all_results[peak_name].items():
        regrets = np.array([t["simple_regret"] for t in trials])
        mean = regrets.mean(axis=0)
        stderr = regrets.std(axis=0) / np.sqrt(len(trials))

        plt.plot(mean, label=kernel_name)
        plt.fill_between(range(len(mean)), mean - stderr, mean + stderr, alpha=0.2)

    plt.xlabel("Iteration")
    plt.ylabel("Simple Regret (m)")
    plt.title(f"Kernel Comparison — {peak_name}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_kernel_landscapes2(all_results, peak_name, trial_idx=0):
    """
    Show the GP predicted surface for each kernel side by side.
    Uses the saved X and Y from a single trial to refit the GP.

    trial_idx: which seed/trial to visualize (default first)
    """
    kernel_names = list(all_results[peak_name].keys())
    n_kernels = len(kernel_names)

    fig, axes = plt.subplots(1, n_kernels, figsize=(6 * n_kernels, 5))
    if n_kernels == 1:
        axes = [axes]

    for ax, kernel_name in zip(axes, kernel_names):
        trial = all_results[peak_name][kernel_name][trial_idx]
        X = trial["X"]
        Y = trial["Y"]

        # Refit GP from saved data
        kernel_map = {
            "RBF": GPy.kern.RBF(input_dim=2),
            "Matern32": GPy.kern.Matern32(input_dim=2),
            "Matern52": GPy.kern.Matern52(input_dim=2),
            "Periodic": GPy.kern.StdPeriodic(input_dim=2),
        }
        kern = kernel_map[kernel_name]
        gp = GPy.models.GPRegression(X, Y, kern)
        gp.optimize_restarts(num_restarts=3, verbose=False)

        # Build prediction grid
        lon_min, lon_max = X[:, 0].min(), X[:, 0].max()
        lat_min, lat_max = X[:, 1].min(), X[:, 1].max()
        # Pad slightly beyond sampled points
        lon_pad = (lon_max - lon_min) * 0.05
        lat_pad = (lat_max - lat_min) * 0.05

        grid_x = np.linspace(lon_min - lon_pad, lon_max + lon_pad, 100)
        grid_y = np.linspace(lat_min - lat_pad, lat_max + lat_pad, 100)
        X1, X2 = np.meshgrid(grid_x, grid_y)
        X_grid = np.column_stack([X1.ravel(), X2.ravel()])

        mean, var = gp.predict(X_grid)
        mean = -mean.reshape(100, 100)  # negate since we minimized -elevation

        extent = [grid_x[0], grid_x[-1], grid_y[0], grid_y[-1]]
        im = ax.imshow(
            mean, cmap="terrain", origin="lower", extent=extent, aspect="auto"
        )
        ax.scatter(
            X[:, 0],
            X[:, 1],
            c="red",
            s=10,
            zorder=5,
            edgecolors="black",
            linewidths=0.5,
        )
        ax.set_title(f"{kernel_name}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        plt.colorbar(im, ax=ax, label="Elevation (m)")

    fig.suptitle(
        f"GP Predicted Surfaces — {peak_name} (trial {trial_idx})", fontsize=14
    )
    plt.tight_layout()
    plt.show()


def plot_predicted_surface(bo, coords, N, true_surface=None):
    """
    coords: (N*N, 2) array of [lon, lat] pairs (same as your meshgrid reshaped)
    N: grid resolution per axis
    """
    mean, var = bo.model.model.predict(coords)
    mean = -mean.reshape(N, N)  # negate since GPyOpt minimizes
    std = np.sqrt(var.reshape(N, N))

    lon_range = [coords[:, 0].min(), coords[:, 0].max()]
    lat_range = [coords[:, 1].min(), coords[:, 1].max()]
    extent = [lon_range[0], lon_range[1], lat_range[0], lat_range[1]]

    fig, axes = plt.subplots(1, 3 if true_surface is not None else 2, figsize=(18, 5))
    idx = 0

    if true_surface is not None:
        axes[idx].imshow(
            true_surface.T, cmap="terrain", origin="lower", extent=extent, aspect="auto"
        )
        axes[idx].set_title("True Surface")
        idx += 1

    axes[idx].imshow(
        mean.T, cmap="terrain", origin="lower", extent=extent, aspect="auto"
    )
    axes[idx].scatter(bo.X[:, 0], bo.X[:, 1], c="red", s=10, zorder=5)
    axes[idx].set_title("GP Predicted Surface")
    idx += 1

    axes[idx].imshow(
        std.T, cmap="viridis", origin="lower", extent=extent, aspect="auto"
    )
    axes[idx].scatter(bo.X[:, 0], bo.X[:, 1], c="red", s=10, zorder=5)


def plot_simple_regret(bo, true_max):
    Y = bo.Y.flatten()
    best_so_far = np.maximum.accumulate(-Y)  # GPyOpt minimizes, so negate
    regret = true_max - best_so_far
    plt.plot(regret)
    plt.xlabel("Iteration")
    plt.ylabel("Simple Regret (m)")
    plt.title("Simple Regret")


def make_equal_area_box(lat, lon, half_km=5):
    """Create a box of approximately half_km × half_km centered on (lat, lon)"""
    lat_half = half_km / 111.0  # 1 deg lat ≈ 111 km
    lon_half = half_km / (111.0 * math.cos(math.radians(lat)))
    return {
        "latitude": (lat - lat_half, lat + lat_half),
        "longitude": (lon - lon_half, lon + lon_half),
    }


def query(points_lonlat, vrt_path="G:\\data\\zipData\\nasadem_all\\nasadem.vrt"):
    with rasterio.open(vrt_path) as src:
        # Reproject input lon/lat -> dataset CRS if needed
        if src.crs and src.crs.to_string() != "EPSG:4326":
            lons, lats = zip(*points_lonlat)
            xs, ys = transform("EPSG:4326", src.crs, lons, lats)
            pts = list(zip(xs, ys))
        else:
            pts = points_lonlat

        # Sample band 1
        vals = [v[0] for v in src.sample(pts)]
        return vals


def BO_results(bo, x, y, N):
    plt.figure("Optimization progress")
    im = plt.imshow(
        y, cmap="viridis", origin="lower", extent=[x[0][0], x[0][-1], x[1][0], x[1][-1]]
    )
    plt.plot(bo.X[:, 0], bo.X[:, 1], "ro:")
    for i, xx in enumerate(bo.X):
        plt.text(xx[0], xx[1], "%i" % (i + 1))
    plt.colorbar(im)
    plt.figure("Approximated function")
    plt.subplot(1, 2, 1)
    plt.title("mean")
    plt.imshow(
        bo.model.predict(x.T)[0].reshape(N, N).T,
        cmap="viridis",
        origin="lower",
        extent=[x[0][0], x[0][-1], x[1][0], x[1][-1]],
    )
    plt.subplot(1, 2, 2)
    plt.title("variance")
    plt.imshow(
        bo.model.predict(x.T)[1].reshape(N, N).T,
        cmap="viridis",
        origin="lower",
        extent=[x[0][0], x[0][-1], x[1][0], x[1][-1]],
    )
    # plt.suptitle('Approximated function')
    plt.figure("Acquisition function")
    plt.imshow(
        -bo.acquisition.acquisition_function(x.T).reshape(N, N).T,
        cmap="viridis",
        origin="lower",
        extent=[x[0][0], x[0][-1], x[1][0], x[1][-1]],
    )
