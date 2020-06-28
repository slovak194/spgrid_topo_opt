file_path="/home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-40-14-r04804__v8_r0400/fem/00044.tcb.zip.bin.stl";

tx = -150;
ty = -300;

translate(v= [tx, 0, 0]) import(file_path);
mirror() translate(v= [tx, 0, 0]) import(file_path);

mirror(v= [0, 1, 0]) translate(v= [tx, ty, 0]) import(file_path);
mirror(v= [0, 1, 0]) mirror() translate(v= [tx, ty, 0]) import(file_path);
