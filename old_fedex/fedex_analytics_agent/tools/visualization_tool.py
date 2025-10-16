"""Visualization tools for shipment data analysis."""

import matplotlib.pyplot as plt
import pandas as pd
import io
import base64


class VisualizationTool:
    """Create visualizations of shipment and location data."""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {'primary': '#1f77b4', 'secondary': '#ff7f0e', 'success': '#2ca02c', 
                       'danger': '#d62728', 'info': '#17becf'}
    
    def create_location_comparison_chart(self, df: pd.DataFrame, metric: str = 'total_shipments', 
                                        title: str = "Location Comparison") -> str:
        """Create bar chart comparing locations."""
        fig, ax = plt.subplots(figsize=(12, 6))
        df['location_label'] = df['city'].str.title() + ', ' + df['state']
        bars = ax.bar(df['location_label'], df[metric], color=self.colors['primary'])
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height):,}',
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Location', fontsize=12, fontweight='bold')
        ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_growth_trend_chart(self, df: pd.DataFrame, top_n: int = 10, 
                                  title: str = "Top Growing Locations") -> str:
        """Create horizontal bar chart showing growth rates."""
        fig, ax = plt.subplots(figsize=(12, 8))
        df_top = df.nlargest(top_n, 'growth_rate_pct').copy()
        df_top['location_label'] = df_top['location'].str.title() + ', ' + df_top['state']
        
        colors = [self.colors['success'] if x > 0 else self.colors['danger'] for x in df_top['growth_rate_pct']]
        bars = ax.barh(df_top['location_label'], df_top['growth_rate_pct'], color=colors)
        
        for i, (bar, val) in enumerate(zip(bars, df_top['growth_rate_pct'])):
            ax.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Growth Rate (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Location', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_demand_heatmap(self, df: pd.DataFrame, value_column: str = 'shipment_count', 
                             title: str = "Demand by Location") -> str:
        """Create demand visualization across locations."""
        fig, ax = plt.subplots(figsize=(14, 8))
        df_sorted = df.nlargest(15, value_column).copy()
        df_sorted['location'] = (df_sorted['city'].str.title() + ', ' + df_sorted['state'] + 
                                ' (' + df_sorted['zip_code'].astype(str) + ')')
        
        values = df_sorted[value_column]
        normalized = (values - values.min()) / (values.max() - values.min())
        colors = plt.cm.YlOrRd(normalized)
        bars = ax.barh(df_sorted['location'], values, color=colors)
        
        for bar, val in zip(bars, values):
            ax.text(val + max(values) * 0.01, bar.get_y() + bar.get_height()/2,
                   f'{int(val):,}', va='center', fontsize=9, fontweight='bold')
        
        ax.set_xlabel(value_column.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel('Location (Zip Code)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_multi_metric_comparison(self, df: pd.DataFrame, metrics: list, 
                                      title: str = "Multi-Metric Comparison") -> str:
        """Create grouped bar chart comparing multiple metrics."""
        fig, ax = plt.subplots(figsize=(14, 7))
        df['location'] = df['city'].str.title() + ', ' + df['state']
        
        # Normalize to 0-100 scale
        df_norm = df[metrics].copy()
        for col in metrics:
            df_norm[col] = ((df_norm[col] - df_norm[col].min()) / 
                          (df_norm[col].max() - df_norm[col].min()) * 100)
        
        x = range(len(df))
        width = 0.8 / len(metrics)
        
        for i, metric in enumerate(metrics):
            offset = (i - len(metrics)/2) * width + width/2
            ax.bar([p + offset for p in x], df_norm[metric], width,
                  label=metric.replace('_', ' ').title())
        
        ax.set_xlabel('Location', fontsize=12, fontweight='bold')
        ax.set_ylabel('Normalized Score (0-100)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(df['location'], rotation=45, ha='right')
        ax.legend(loc='upper left', frameon=True)
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_demand_gap_visualization(self, df: pd.DataFrame, 
                                       title: str = "High Demand Areas") -> str:
        """Visualize demand gaps for site selection."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        df_top = df.nlargest(10, 'demand_score').copy()
        df_top['location'] = (df_top['city'].str.title() + '\n' + df_top['state'] + 
                             ' ' + df_top['zip_code'].astype(str))
        
        # Left: Demand Score
        colors1 = plt.cm.RdYlGn((df_top['demand_score'] - df_top['demand_score'].min()) / 
                                (df_top['demand_score'].max() - df_top['demand_score'].min()))
        bars1 = ax1.barh(df_top['location'], df_top['demand_score'], color=colors1)
        
        for bar, val in zip(bars1, df_top['demand_score']):
            ax1.text(val + max(df_top['demand_score']) * 0.01, bar.get_y() + bar.get_height()/2,
                    f'${val:,.0f}', va='center', fontsize=9, fontweight='bold')
        
        ax1.set_xlabel('Demand Score ($)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Location', fontsize=11, fontweight='bold')
        ax1.set_title('Total Demand Potential', fontsize=12, fontweight='bold')
        
        # Right: Customers vs Shipments
        scatter = ax2.scatter(df_top['unique_customers'], df_top['shipment_count'],
                            s=df_top['demand_score']/5, c=df_top['avg_order_value'],
                            cmap='viridis', alpha=0.6, edgecolors='black', linewidth=1)
        
        for idx, row in df_top.iterrows():
            ax2.annotate(f"{row['city'].title()}\n{row['zip_code']}", 
                        (row['unique_customers'], row['shipment_count']),
                        fontsize=8, ha='center')
        
        ax2.set_xlabel('Unique Customers', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Shipment Count', fontsize=11, fontweight='bold')
        ax2.set_title('Customer Base vs Activity\n(Bubble size = Demand Score)', 
                     fontsize=12, fontweight='bold')
        
        cbar = plt.colorbar(scatter, ax=ax2)
        cbar.set_label('Avg Order Value ($)', fontsize=10, fontweight='bold')
        
        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_base64
    
    def format_dataframe_for_display(self, df: pd.DataFrame) -> str:
        """Format DataFrame as readable text table."""
        if df.empty:
            return "No data found."
        
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = df[col].round(2)
        
        return df.to_string(index=False)
