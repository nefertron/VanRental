
function displayFetchedImages(imageArray) {
    updateCarousel(imageArray); // create a div in carousel container which will display the to_upload images
    updateCarouselIndicators(imageArray)
}

// create a div which will display the images inside the carousel
function updateCarousel(imageArray) {   
    const carouselItemsContainer = document.getElementById("fetched-carousel-inner");
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
}


function updateCarouselIndicators(imageArray) {
    const carouselIndicators = document.getElementById("fetched-carousel-indicators");
    carouselIndicators.innerHTML = "";

    for (let i = 0; i < imageArray.length; i++) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.bsTarget = "#rent_van";
        button.dataset.bsSlideTo = i;
        if (i === 0) {
            button.classList.add("active");
        }

        carouselIndicators.appendChild(button);
    }
}
