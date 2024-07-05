# BlenderUmap2 QoL Plugin!
Just a bunch of QoL stuff I made working with Minshu's [BlenderUmap2](https://github.com/MinshuG/BlenderUmap2)

This was written for **Blender 4.1**! May not work for older version. I dunno.

# Requirements
* Blender 4.1 (Probably)
* [BlenderUmap2](https://github.com/MinshuG/BlenderUmap2)

# Installation
1. Head to [Releases](https://github.com/jaxbline/Umap-Utilites/releases)
2. Download the latest
3. Open Blender
4. Goto preferences
5. Add-ons
6. Install
7. Install Plugin
8. Profit

# Features
Most buttons are based of Selection. There is a "Apply to All" button that will preform the action to all meshes in your scene!

![image](https://github.com/jaxbline/BlenderUmap2-Utilities/assets/65150735/bec8c549-a004-49c4-9e30-0773307a1f16)


**Make instance Real**
* This does exactly what the name says. Makes all Instances.. real?

**Make Single User**
* Makes the active object into a single user by unlinking it.
> Works with "Apply to All"

**Join Meshes**

* This button will join meshes to your current selected Bbject based off materials
> If "Apply to All" is enabled the Plugin will group all Objects in your scene based off their materials

**Merge Vertcies by Distance**
* Automically merge verts by the selected amount to your current selected Objects
> "Apply to All" works with this too!


**Hide After Join**
* When enabled this hides the mesh after they are joined together... Just makes thing easier shuffle through

**Apply to All**
* When enabled will apply the action to ALL meshes rather then the current selected one.

**Fix Materials**
* This feature will attempt to fix the "Generic Shader" issue when you import a Umap. This is mainly useful for embeded materials into your FBX.

To use this your textures *must* have a suffix at the end of their name. 

```TextureNameHere_di / TextureNameHere_no / TextureNameHere_mr / TextureNameHere_e```


There are 4 Inputs currently
* Diffuse
* Normals
* Metallic/Roughness
* Emission

![image](https://github.com/jaxbline/BlenderUmap2-Utilities/assets/65150735/7244c155-5242-4cca-97ef-ff88a6e1c731)


