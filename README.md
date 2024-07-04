# BlenderUmap2 QoL Plugin!
Just a bunch of QoL stuff I made working with Minshu [BlenderUmap2](https://github.com/MinshuG/BlenderUmap2)

This was made for Blender 4.1! I dunno how it will act for older versions of Blender.



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

![image](https://github.com/jaxbline/Umap-Utilites/assets/65150735/ccb1eea4-6f5e-4d8e-8537-bc7a5c97a52a)

**Make instance Real**
* This does exactly what the name says. Makes all Instances.. real?

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

There are 3 Inputs currently
* Diffuse
* Normals
* Metallic/Roughness

![image](https://github.com/jaxbline/Umap-Utilites/assets/65150735/0bb9a799-0be3-42c1-8e3a-694118bf3fb3)

*TextureNameHere_Diffuse* / *TextureNameHere_Normal* / *TextureNameHere_MR*
