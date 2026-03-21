# Key Mapping  

If you want to remap keys to other keys or key sequences, the recommended approach is to use **input-remapper**. It is a powerful tool for key remapping and customization.  
For more information, visit the [input-remapper GitHub page](https://github.com/sezanzeb/input-remapper?tab=readme-ov-file).  

### Alternative Tools  

1. **xmodmap**:  
   If you only need to map a single key to another single key, you can use `xmodmap`.  
   - This tool supports remapping keys to various functions but does not allow mapping keys to strings.  
   - Refer to the [xmodmap Arch Wiki page](https://wiki.archlinux.org/title/Xmodmap) for detailed instructions.  

2. **Bash Bind Command**:  
   In bash, you can remap keys using the `bind` command.  
   - Official documentation: [Bash Builtins Manual](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)  
   - For a more explanatory guide with examples, see [this article](https://ioflood.com/blog/bind-linux-command/).  

---

# Creating a BMP Image for `loadicon`  

The `loadicon` program requires images in BMP format with the following specifications:  
- Maximum dimensions: **64x64 pixels**  
- Pixel format: **RGB565**  

You can use **GIMP** to create these images. Follow the steps below to convert an image to the required format:  

1. **Open the Image**:  
   - Launch GIMP and load your image (e.g., in JPEG or PNG format).  

2. **Resize the Image**:  
   - From the **Image** dropdown menu, select **Scale Image**.  
   - In the dialog box that appears:  
     - Set the width and height to a maximum of **64 pixels**.  
     - To change the aspect ratio, click the connector icon next to the width and height input fields.  
   - Click **Scale** after setting the dimensions.  

3. **Export the Image**:  
   - Go to the **File** dropdown menu and select **Export As...**.  
   - Enter a filename with the `.bmp` extension.  
   - Click **Export** to proceed.  

4. **Set BMP Options**:  
   - In the "Export Image as BMP" dialog box:  
     - Click **Advanced Options**.  
     - Select **16 bits** and check the box for **R5 G6 B5**.  
   - Press **Export** to generate the BMP image.  

Your BMP image is now ready to use with `loadicon`.  
