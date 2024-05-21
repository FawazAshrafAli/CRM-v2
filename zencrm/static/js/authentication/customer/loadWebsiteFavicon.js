function loadWebsiteFavicon(input) {    
    var faviconPreviewBoxDisplay = document.getElementById('favicon-preview-box').style.display
    if (faviconPreviewBoxDisplay == 'none') {        
        document.getElementById('favicon-preview-box').style.display="flex";
        // document.getElementById('favicon-preview-box').style.alignItems = 'center';
    }
    var file = input.files[0];
    var imageUrl = URL.createObjectURL(file);
    document.getElementById('website-favicon-preview').setAttribute('src', imageUrl);
}