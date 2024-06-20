import waldbrand
from viz import df_viz

waldbrand_obj = waldbrand.WildFire()
forest_fire_areas_df = waldbrand_obj.get_all_ffa()
db_causes = waldbrand_obj.get_all_causes()
viz_obj = df_viz.DataFrameVisualizer(forest_fire_areas_df)
causes_viz = df_viz.DataFrameVisualizer(db_causes)
# viz_obj.plot_scatter("Year", "Zusammen Anzahl ", plot_avg=True)
causes_viz.lineplot()
