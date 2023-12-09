
function displayPendingUploadedPreview(event) {
    const files = event.target.files;
    const imageArray = [];

    for (let i = 0; i < files.length; i++) {
        console.log('file' , files[i])
        const reader = new FileReader();
        reader.onload = function (e) {
            imageArray.push(e.target.result);
            if (imageArray.length === files.length) {
                updateCarousel(imageArray); // create a div in carousel container which will display the to_upload images
                updatePendingImagesSrcContainer(imageArray);   // update the value of images input field (hidden) which will be used in the backend
                updateCarouselIndicators(imageArray)
            }
        };
        reader.readAsDataURL(files[i]);
    }
}

// create a div which will display the images inside the carousel
function updateCarousel(imageArray) {   
    const carouselItemsContainer = document.getElementById("carousel-inner");
    carouselItemsContainer.innerHTML = "";

    for (let i = 0; i < imageArray.length; i++) {
        const carouselItem = document.createElement("div");

        if (i === 0){
            carouselItem.classList.add("carousel-item");
            carouselItem.classList.add("active");
        }
        else{
            carouselItem.classList.add("carousel-item");
        }
        
        const imageContainer = document.createElement("div")
        imageContainer.classList.add('slider-image-container')

        const imageElement = document.createElement("img");
        imageElement.src = imageArray[i];
        imageElement.classList.add("slider-image");

        imageContainer.appendChild(imageElement);
        carouselItem.appendChild(imageContainer);
        carouselItemsContainer.appendChild(carouselItem);
    }

    document.getElementById('carousel_title').textContent = 'Van Images'
}


function updateCarouselIndicators(imageArray) {
    const carouselIndicators = document.getElementById("carousel-indicators");
    carouselIndicators.innerHTML = "";

    for (let i = 0; i < imageArray.length; i++) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.bsTarget = "#add_van";
        button.dataset.bsSlideTo = i;
        if (i === 0) {
            button.classList.add("active");
        }

        carouselIndicators.appendChild(button);
    }
}

function updatePendingImagesSrcContainer(imageArray) {
    const hiddenInput = document.querySelector('input[name="pending_images"]');
    hiddenInput.value = imageArray.join('|||');
}