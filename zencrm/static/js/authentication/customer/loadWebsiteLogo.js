function loadWebsiteLogo(input) {
    var logoPreviewBoxDisplay = document.getElementById('logo-preview-box').style.display
    if (logoPreviewBoxDisplay == 'none') {        
        document.getElementById('logo-preview-box').style.display="flex";
        // document.getElementById('logo-preview-box').style.alignItems = 'center';
    }
    var file = input.files[0];
    var imageUrl = URL.createObjectURL(file);
    document.getElementById('website-logo-preview').setAttribute('src', imageUrl);
}

