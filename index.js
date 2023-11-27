const referenceCanvasId = "referenceCanvas";
const displayCanvasId = "displayCanvas";
const workingCanvasId = "workingCanvas";

const internalResolution = 75;
const displayResolution = 256;


class Individual {

}

class GeneticAlgorithm {
    constructor(referenceCanvas, displayCanvas, workingCanvas) {
        this.referenceCanvas = referenceCanvas;
        this.displayCanvas = displayCanvas;
        this.workingCanvas = workingCanvas;

    }
    setup() {

    }
}

class Page {
    setupImage() {

    }

    configureCanvas(canvas, resolution) {
        canvas.width = resolution;
        canvas.height = resolution;
        canvas.style.width = resolution;
        canvas.style.height = resolution;
    }
    
    setup() {
        console.log('Setting up!');

        const referenceCanvas = document.getElementById(referenceCanvasId);
        const displayCanvas = document.getElementById(displayCanvasId);
        const workingCanvas = document.getElementById(workingCanvasId);
        const referenceContext = referenceCanvas.getContext('2d');
        const displayContext = displayCanvas.getContext('2d');
        const workingContext = workingCanvas.getContext('2d');

        this.configureCanvas(referenceCanvas, displayResolution);
        this.configureCanvas(displayCanvas, displayResolution);
        this.configureCanvas(workingCanvas, internalResolution);
    }
}



function setup() {
    console.log('starting');
    const referenceCanvas = document.getElementById(referenceCanvasId);
    const displayCanvas = document.getElementById(displayCanvasId);
    const workingCanvas = document.getElementById(workingCanvasId);
    const referenceContext = referenceCanvas.getContext('2d');
    const displayContext = displayCanvas.getContext('2d');
    const workingContext = workingCanvas.getContext('2d');
    // configureCanvas(referenceCanvas, displayResolution);
    // configureCanvas(displayCanvas, displayResolution);
    // configureCanvas(workingCanvas, internalResolution);

    const image = new Image();
    image.onload = configureImage
}


const page = new Page()
page.setup();
window.onload = page.setup;