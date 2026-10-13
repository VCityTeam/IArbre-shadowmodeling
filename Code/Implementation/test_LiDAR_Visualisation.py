import pdal
import json
# import kaleido
import numpy as np
import plotly.graph_objects as go


def visualize_pointcloud(laz_file_path, sample_size=None):

    # https://medium.com/@BlanchR2/visualize-your-city-in-3d-a-quick-guide-to-lidar-point-clouds-in-python-00ae3cb2741b

    # Create PDAL pipeline to read LAZ file
    pipeline = pdal.Pipeline(json.dumps({
        "pipeline": [
            laz_file_path,
            {
                "type": "filters.range",
                "limits": "Classification[8:8]"
            },
            {  # filtre
                "type": "filters.assign",
                "value": "Y=0"
            }
        ]
    }))
    # Execute pipeline
    pipeline.execute()
    # Print type
    pointsCloud = pipeline.arrays[0]
    print(pointsCloud.dtype.names)


    #print(pointsCloud['Classification'])
    #print(pointsCloud['Z'])
    """         { #filtre
                    "type": "filters.assign",
                    "value": "Classification = Z"
                },
                {  # filtre
                    "type": "filters.assign",
                    "value": "Z=0"
                }
                {
                "type": "filters.range",
                "limits": "Classification[0:0]"
                }
    """
    #pointsCloud['Z'] = 0
    # print(points)



    # Get point cloud data
    arrays = pipeline.arrays[0]
    points = np.vstack((arrays['X'], arrays['Y'], arrays['Z'])).transpose()

    # Sample points if specified
    if sample_size and sample_size < len(points):
        indices = np.random.choice(len(points), sample_size, replace=False)
        points = points[indices]

    # Create 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(
            size=1,
            opacity=0.8,
            #color=points[:, 2],
            color = pointsCloud['Classification'],
            colorscale='jet',
            showscale=True
        )
    )])

    fig.update_layout(
        scene=dict(
            aspectmode='data'
        ),
        width=1000,
        height=800
    )

    #fig.write_image("fig.png")

    fig.show()


# run the code
visualize_pointcloud("18455_51780.laz", sample_size=100000) #100000
