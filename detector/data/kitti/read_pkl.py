import pickle

info_path="/workspaces/pointpainting_docker/PointPainting_test/detector/data/kitti/kitti_infos_train_v1.pkl"
with open(info_path, 'rb') as f:
    infos = pickle.load(f)
info_path_v2="/workspaces/pointpainting_docker/PointPainting_test/detector/data/kitti/kitti_infos_train_v2.pkl"
with open(info_path_v2,'rb') as f:
    infos_v2=pickle.load(f)
db_infos_test_path="/workspaces/pointpainting_docker/PointPainting_test/detector/data/kitti/kitti_dbinfos_train.pkl"
with open(db_infos_test_path,'rb') as f:
    infos_v3=pickle.load(f)
print("yes")