const fileTypes = [
  	"image/apng",
	 "image/bmp",
  	"image/gif",
  	"image/jpeg",
  	"image/pjpeg",
  	"image/png",
  	"image/svg+xml",
  	"image/tiff",
  	"image/webp",
  	"image/x-icon"
	];
	function validFileType(file) {
	  	return fileTypes.includes(file.type);
	}

	function returnFileSize(number) {
  		if (number < 1024) {
	    	return `${number} bytes`;
  		} else if (number >= 1024 && number < 1048576) {
	    	return `${(number / 1024).toFixed(1)} KB`;
  		} else if (number >= 1048576) {
    		return `${(number / 1048576).toFixed(1)} MB`;
  		}
	}


	document.querySelector("#userprofile").onchange = function(event) {
		let archivo = event.target.files[0];
		if(archivo.length === 0) {
			console.log("No seleciono el avatar");
		} else {
			if(validFileType(archivo)) {
				let vista =  document.querySelector("#vista-userprofile");
				vista.src = URL.createObjectURL(archivo);
				console.log(returnFileSize(archivo.size));
			} else {
				console.log("Tipo de archivo no valido");
			}
		}
	}