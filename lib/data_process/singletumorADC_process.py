from monai import transforms
import numpy as np
import os
import glob
import nibabel as nib

# Single tumor ADC MRI:800 ~ 3600 Size:32x256x256
train_path = "/media/data1/jiachuang/data/medical/301segmentation_singletumor_t/train/ADC"
train_label_path = "/media/data1/jiachuang/data/medical/301segmentation_singletumor_t/label/ADC"
val_path = "/media/data1/jiachuang/data/medical/301segmentation_singletumor_v/train/ADC"
val_label_path = "/media/data1/jiachuang/data/medical/301segmentation_singletumor_v/label/ADC"

if __name__ == '__main__':

    list_train = sorted(glob.glob(os.path.join(train_path, '*.nii.gz')))
    label_train = sorted(glob.glob(os.path.join(train_label_path, '*.nii.gz')))
    list_val = sorted(glob.glob(os.path.join(val_path, '*.nii.gz')))
    label_val = sorted(glob.glob(os.path.join(val_label_path, '*.nii.gz')))

    train_data_dicts = [
        {"image": image_name, "label": label_name}
        for image_name, label_name in zip(list_train, label_train)
    ]

    val_data_dicts = [
        {"image": image_name, "label": label_name}
        for image_name, label_name in zip(list_val, label_val)
    ]

    original_transform = transforms.Compose(
        [
            transforms.LoadImaged(keys=["image", "label"]),
            transforms.AddChanneld(keys=["image", "label"]),
            transforms.CropForegroundd(keys=["image", "label"], source_key="image"),
            transforms.CenterSpatialCropd(
                keys=["image", "label"],
                roi_size=(32, 256, 256),
            ),
            transforms.ScaleIntensityRanged(keys=["image"],
                                            a_min=800.0,
                                            a_max=3600.0,
                                            b_min=0.0,
                                            b_max=1.0,
                                            clip=True),
            transforms.SpatialPadD(keys=["image", "label"],
                                   spatial_size=(32, 256, 256),
                                   method='symmetric',
                                   mode='constant'),
        ]
    )

    train_transform = transforms.Compose(
        [
            transforms.LoadImaged(keys=["image", "label"]),
            transforms.AddChanneld(keys=["image", "label"]),
            transforms.Orientationd(keys=["image", "label"],
                                    axcodes="RAS"),
            transforms.CropForegroundd(keys=["image", "label"], source_key="image"),
            transforms.CenterSpatialCropd(
                keys=["image", "label"],
                roi_size=(32, 256, 256),
            ),
            transforms.RandFlipd(keys=["image", "label"],
                                 prob=1.0,
                                 spatial_axis=0),
            transforms.RandFlipd(keys=["image", "label"],
                                 prob=1.0,
                                 spatial_axis=1),
            transforms.RandFlipd(keys=["image", "label"],
                                 prob=1.0,
                                 spatial_axis=2),
            transforms.RandRotate90d(
                keys=["image", "label"],
                prob=0.5,
                max_k=3,
                spatial_axes=(1, 2)
            ),
            transforms.RandScaleIntensityd(keys="image",
                                           factors=0.1,
                                           prob=0.5),
            transforms.RandShiftIntensityd(keys="image",
                                           offsets=0.1,
                                           prob=0.5),

            transforms.ScaleIntensityRanged(keys=["image"],
                                            a_min=800.0,
                                            a_max=3600.0,
                                            b_min=0.0,
                                            b_max=1.0,
                                            clip=True),
            transforms.SpatialPadD(keys=["image", "label"],
                                   spatial_size=(32, 256, 256),
                                   method='symmetric',
                                   mode='constant'),
        ]
    )
    val_transform = transforms.Compose(
        [
            transforms.LoadImaged(keys=["image", "label"]),
            transforms.AddChanneld(keys=["image", "label"]),
            transforms.CropForegroundd(keys=["image", "label"],
                                       source_key="image"),
            transforms.CenterSpatialCropd(
                keys=["image", "label"],
                roi_size=(32, 256, 256),
            ),

            transforms.ScaleIntensityRanged(keys=["image"],
                                            a_min=800.0,
                                            a_max=3600.0,
                                            b_min=0.0,
                                            b_max=1.0,
                                            clip=True),
            transforms.SpatialPadD(keys=["image", "label"],
                                   spatial_size=(32, 256, 256),
                                   method='symmetric',
                                   mode='constant'),
        ]
    )
    print("====Start Augmentation====")

    # aug_train = train_transform(train_data_dicts)
    # ori_train = original_transform(train_data_dicts)
    aug_val = val_transform(val_data_dicts)
    # training dataset augmentation Single tumor ADC
    # for i in range(len(list_train)):
    #     img_save = aug_train[i]['image'].squeeze(0).detach().cpu().numpy()
    #     lab_save = aug_train[i]['label'].squeeze(0).detach().cpu().numpy()
    #     print(f"t_a image shape: {img_save.shape}", "type:", type(img_save), "max_min", aug_train[i]['image'].max(),
    #           aug_train[i]['image'].min())
    #     print(f"t_a lab shape: {lab_save.shape}", type(lab_save), "max_min", aug_train[i]['label'].max(),
    #           aug_train[i]['label'].min())
    #     new_img = nib.Nifti1Image(img_save, np.eye(4))
    #     nib.save(new_img,
    #              '/media/data1/jiachuang/projects/kidney/data/single/ADC/train/img/aug_{}.nii.gz'.format(i))
    #     new_lab = nib.Nifti1Image(lab_save, np.eye(4))
    #     nib.save(new_lab,
    #              '/media/data1/jiachuang/projects/kidney/data/single/ADC/train/label/aug_{}.nii.gz'.format(i))
    # print("Training dataset augmentation transformed FINISH.")

    # training dataset original crop Single tumor ADC
    # for i in range(len(list_train)):
    #     img_save = ori_train[i]['image'].squeeze(0).detach().cpu().numpy()
    #     lab_save = ori_train[i]['label'].squeeze(0).detach().cpu().numpy()
    #     print(f"t_o image shape: {img_save.shape}", "type:", type(img_save), "max_min", ori_train[i]['image'].max(),
    #           ori_train[i]['image'].min())
    #     print(f"t_o lab shape: {lab_save.shape}", type(lab_save), "max_min", ori_train[i]['label'].max(),
    #           ori_train[i]['label'].min())
    #     new_img = nib.Nifti1Image(img_save, np.eye(4))
    #     nib.save(new_img,
    #              '/media/data1/jiachuang/projects/kidney/data/single/ADC/train/img/ori_{}.nii.gz'.format(i))
    #     new_lab = nib.Nifti1Image(lab_save, np.eye(4))
    #     nib.save(new_lab,
    #              '/media/data1/jiachuang/projects/kidney/data/single/ADC/train/label/ori_{}.nii.gz'.format(i))
    # print("Training dataset augmentation transformed FINISH.")


    # validating dataset augmentation Single tumor ADC
    for i in range(len(list_val)):
        img_save = aug_val[i]['image'].squeeze(0).detach().cpu().numpy()
        lab_save = aug_val[i]['label'].squeeze(0).detach().cpu().numpy()
        print(f"v image shape: {img_save.shape}", "type:", type(img_save), "max_min", aug_val[i]['image'].max(),
              aug_val[i]['image'].min())
        print(f"v lab shape: {lab_save.shape}", type(lab_save), "max_min", aug_val[i]['label'].max(),
              aug_val[i]['label'].min())
        new_img = nib.Nifti1Image(img_save, np.eye(4))
        nib.save(new_img, '/media/data1/jiachuang/projects/kidney/data/single/ADC/val/img/{}_{}.nii.gz'.format(str(i).zfill(2), list_val[i].split("/")[-1].split(".")[0]))
        new_lab = nib.Nifti1Image(lab_save, np.eye(4))
        nib.save(new_lab, '/media/data1/jiachuang/projects/kidney/data/single/ADC/val/label/{}_{}.nii.gz'.format(str(i).zfill(2), list_val[i].split("/")[-1].split(".")[0]))
    print("Validating dataset transformed FINISH.")
