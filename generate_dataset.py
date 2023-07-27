import omni.replicator.core as rep
import datetime

now = datetime.datetime.now()

# Camera1
focal_length1 = 25
focus_distance1 = 1200
f_stop1 = 0.4
pixel_resolution1 = (512, 512)
horizontal_aperture1 = 8.5
camera1_pos = [(0, 270, 500), (500, 270, 500), (-500, 270, 500)]


# Camera2 (Top view)
focal_length2 = 50
focus_distance2 = 5000
f_stop2 = 2.8
pixel_resolution2 = (512, 512)
horizontal_aperture2 = 8.5
camera2_pos = [(0, 1800, 0)]

with rep.new_layer():
    # Camera1
    camera1 = rep.create.camera(
        position=(0, 0, 1200),
        rotation=(0, -90, 0),
        focal_length=focal_length1,
        focus_distance=focus_distance1,
        f_stop=f_stop1,
        horizontal_aperture=horizontal_aperture1,
        name='Camera1'
    )

    # Camera2
    camera2 = rep.create.camera(
        position=(0, 1500, 0),
        rotation=(-90, 0, 0),
        focal_length=focal_length2,
        focus_distance=focus_distance2,
        f_stop=f_stop2,
        horizontal_aperture=horizontal_aperture2,
        name='Camera2'
    )

    # Create a new render_product (1 for each camera)
    render_product1 = rep.create.render_product(camera1, pixel_resolution1)
    render_product2 = rep.create.render_product(camera2, pixel_resolution2)


    # Create the floor plane
    floor = rep.create.plane(
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(50, 50, 50),
        semantics=[('class', 'floor')],
        name='floor',
    )

    # Randomize the floor material
    def random_Floor_Material():
        floor_material = rep.randomizer.materials(
            materials=rep.get.material(path_pattern="/Fire/Looks/*"),
            input_prims=floor
        )
        return floor_material.node
    rep.randomizer.register(random_Floor_Material)

    with rep.trigger.on_frame(num_frames=300):
        rep.randomizer.random_Floor_Material()
        with camera1:
            rep.modify.pose(look_at=(0, 0, 0), position=rep.distribution.sequence(camera1_pos))
        with camera2:
            rep.modify.pose(look_at=(0, 0, 0), position=rep.distribution.sequence(camera2_pos))

writer = rep.WriterRegistry.get("BasicWriter")
now = now.strftime("%Y-%m-%d")
output_dir = "fire_data_" + now
writer.initialize(output_dir=output_dir, rgb=True)
writer.attach([render_product1, render_product2])
