import open3d as o3d

def render_ply_to_image(ply_path, image_path='output.png', width=1024, height=768):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(ply_path)

    # Visualizer without interactive window
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False, width=width, height=height)
    vis.add_geometry(pcd)

    vis.poll_events()
    vis.update_renderer()

    # Save image
    vis.capture_screen_image(image_path)
    vis.destroy_window()
    print(f"Saved rendered image to {image_path}")


#render_ply_to_image("point_cloud.ply", "rendered_view.png")

import open3d as o3d

# Load the point cloud
pcd = o3d.io.read_point_cloud("point-cld.ply")  # Replace with your actual filename

# Print some information
print(pcd)
print("Has colors:", pcd.has_colors())

# Visualize
o3d.visualization.draw_geometries(
    [pcd],
    zoom=0.5,
    front=[0.0, 0.0, -1.0],
    lookat=[0.0, 0.0, 0.0],
    up=[0.0, -1.0, 0.0]
)