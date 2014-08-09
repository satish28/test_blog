function imgError(image) {
	/* This is the path for default gravatar image.
	This file is added in settings.py for reference. */
	var default_gravatar_image = "/static/common/images/hacker.jpg";
	
    image.onerror = "";
    image.src = default_gravatar_image;
    return true;
}