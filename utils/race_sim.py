import plotly.express as px
import pandas as pd

# Example data loading
df = pd.read_csv('/mnt/data/lap_times.csv')

# Preprocessing to simplify the example
df = df[df['raceId'] == 841]  # Filter for a specific race for demonstration

# Creating the animated scatter plot
fig = px.scatter(df, x="lap", y="position", animation_frame="lap", animation_group="driverId",
                 size_max=55, range_y=[df.position.max(), df.position.min()],
                 labels={"position": "Position", "lap": "Lap Number"})

# Enhancing the plot
fig.update_layout(title="F1 Race Position Animation",
                  xaxis_title="Lap Number",
                  yaxis_title="Position",
                  showlegend=False)

# Show the plot
fig.show()
