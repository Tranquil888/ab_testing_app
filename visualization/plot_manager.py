"""
Управление графиками matplotlib для приложения A/B тестирования.
Реализовано в процедурном стиле без использования классов.

Все созданные фигуры и канвасы хранятся в модульных словарях,
чтобы их можно было сохранять и переиспользовать.
"""

import os
import sys
from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import translator


FIGURES: Dict[str, plt.Figure] = {}
CANVASES: Dict[str, FigureCanvasTkAgg] = {}


def create_simulation_histogram(parent_frame, simulation_data: Dict[str, Any]) -> FigureCanvasTkAgg:
    """Создать гистограмму результатов симуляции."""
    fig, ax = plt.subplots(figsize=(10, 6))

    p_diffs = simulation_data['p_diffs']
    actual_diff = simulation_data['actual_diff']
    p_value = simulation_data['p_value']

    ax.hist(p_diffs, bins=200, alpha=0.7, color='skyblue', edgecolor='black')

    ax.axvline(
        actual_diff,
        color='red',
        linewidth=2,
        label=translator.t('plot_simulation_actual_diff', actual_diff),
    )
    ax.axvline(
        0,
        color='black',
        linestyle='--',
        alpha=0.5,
        label=translator.t('plot_simulation_null_hypothesis'),
    )

    ax.set_xlabel(translator.t('plot_simulation_xlabel'), fontsize=12)
    ax.set_ylabel(translator.t('plot_simulation_ylabel'), fontsize=12)
    ax.set_title(translator.t('plot_simulation_title'), fontsize=14, fontweight='bold')

    ax.text(
        0.02,
        0.98,
        translator.t('plot_simulation_p_value', p_value),
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
    )

    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.005, 0.005)

    canvas = FigureCanvasTkAgg(fig, parent_frame)
    canvas.draw()

    FIGURES['simulation'] = fig
    CANVASES['simulation'] = canvas

    return canvas


def create_conversion_comparison_chart(parent_frame, stats: Dict[str, Any]) -> FigureCanvasTkAgg:
    """Создать столбчатую диаграмму сравнения конверсий."""
    fig, ax = plt.subplots(figsize=(8, 6))

    groups = [
        translator.t('plot_comparison_control'),
        translator.t('plot_comparison_treatment'),
    ]
    ylabel = translator.t('plot_comparison_ylabel')
    title = translator.t('plot_comparison_title')

    conversion_rates = [stats['control_conversion'], stats['treatment_conversion']]
    colors = ['lightcoral', 'lightblue']

    bars = ax.bar(groups, conversion_rates, color=colors, alpha=0.8, edgecolor='black')

    for bar, rate in zip(bars, conversion_rates):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.001,
            f'{rate:.4f}',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold',
        )

    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(conversion_rates) * 1.2)
    ax.grid(True, alpha=0.3, axis='y')

    canvas = FigureCanvasTkAgg(fig, parent_frame)
    canvas.draw()

    FIGURES['comparison'] = fig
    CANVASES['comparison'] = canvas

    return canvas


def create_time_series_plot(parent_frame, time_data: pd.DataFrame) -> FigureCanvasTkAgg:
    """Создать временной график конверсии."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    xlabel = translator.t('plot_time_series_xlabel')
    ylabel = translator.t('plot_time_series_ylabel')
    title1 = translator.t('plot_time_series_title1')
    title2 = translator.t('plot_time_series_title2')
    diff_ylabel = translator.t('plot_time_series_diff_ylabel')
    old_page_label = translator.t('plot_time_series_old_page')
    new_page_label = translator.t('plot_time_series_new_page')

    ax1.scatter(time_data['day'], time_data['old_rate'], color='green', label=old_page_label, alpha=0.7, s=50)
    ax1.scatter(time_data['day'], time_data['new_rate'], color='red', label=new_page_label, alpha=0.7, s=50)

    ax1.set_xlabel(xlabel, fontsize=11)
    ax1.set_ylabel(ylabel, fontsize=11)
    ax1.set_title(title1, fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.scatter(
        time_data['day'],
        time_data['new_rate'] - time_data['old_rate'],
        color='blue',
        alpha=0.7,
        s=50,
    )
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)

    ax2.set_xlabel(xlabel, fontsize=11)
    ax2.set_ylabel(diff_ylabel, fontsize=11)
    ax2.set_title(title2, fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, parent_frame)
    canvas.draw()

    FIGURES['time_series'] = fig
    CANVASES['time_series'] = canvas

    return canvas


def create_day_of_week_chart(parent_frame, dow_data: pd.DataFrame) -> FigureCanvasTkAgg:
    """Создать диаграмму конверсии по дням недели."""
    fig, ax = plt.subplots(figsize=(10, 6))

    days = dow_data.index.tolist()
    rates = dow_data['conversion_rate'].values

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(days)))

    bars = ax.bar(days, rates, color=colors, alpha=0.8, edgecolor='black')

    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.0005,
            f'{rate:.4f}',
            ha='center',
            va='bottom',
            fontsize=10,
            rotation=45,
        )

    ylabel = translator.t('plot_day_of_week_ylabel')
    title = translator.t('plot_day_of_week_title')

    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, parent_frame)
    canvas.draw()

    FIGURES['day_of_week'] = fig
    CANVASES['day_of_week'] = canvas

    return canvas


def clear_all_plots():
    """Очистить все сохранённые фигуры и канвасы."""
    for fig in FIGURES.values():
        plt.close(fig)
    FIGURES.clear()
    CANVASES.clear()


def save_plot(plot_name: str, filename: str) -> bool:
    """Сохранить конкретный график в файл."""
    if plot_name in FIGURES:
        FIGURES[plot_name].savefig(filename, dpi=300, bbox_inches='tight')
        return True
    return False
