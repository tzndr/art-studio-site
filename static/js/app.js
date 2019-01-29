//Declaring global variables


var ViewModel = function() {
  var self = this;

  var currentImage = 0;

  var imageElement = document.getElementById('image-changer');

  function nextImage(){
      currentImage = (currentImage + 1) % mainImages.length;
      imageElement.src = mainImages[currentImage];
  }

  var timeoutId = setTimeout(nextImage, 1000);

}
