// Original code by Chris Cummins (https://chriscummins.cc/s/genetics/). This is just a reimplementation

// Configuration
const internalResolution = 75;
const displayResolution = 256;
const pixelDataSize = internalResolution * internalResolution * 4

const numberOfPolygons = 125;
const numberOfVertices = 3;
const geneSize = 4 + numberOfVertices * 2; // 4 for colour, 6 for positions
const dnaSize = numberOfPolygons * geneSize;

const populationSize = 50;
const selectionCutoff = 0.15;
const mutationChance = 0.01;
const mutationAmount = 0.1;

// Canvas
let referenceCanvas = null;
let referenceContext = null;
let outputCanvas = null;
let outputContext = null;
let workingCanvas = null;
let workingContext = null;
let generationElement = null;
let fitnessElement = null;

let generation = 0;
let imageData = null;
let population = null;

function setCanvasProperties(canvas, resolution) {
    canvas.width = resolution;
    canvas.height = resolution;
    canvas.style.width = resolution;
    canvas.style.height = resolution;
}

class Individual {
    dna = [];
    fitness = -1;


    constructor(father = null, mother = null) {

        if (father && mother) {
            // Inherit genes from parents
            for (let g = 0; g < dnaSize; g+= geneSize) {
                const parent = (Math.random() < 0.5) ? father : mother;
                for (let i = 0; i < geneSize; i++) {
                    let gene = parent.dna[g+i];
                    if (Math.random() < mutationChance) {
                        const mutation = Math.random() * mutationAmount * 2 - mutationAmount;
                        gene += mutation;
                        if (gene < 0) {
                            gene = 0;
                        }
                        if (gene > 1) {
                            gene = 1;
                        }
                    }
                    this.dna.push(gene);
                }
            }
        } else {
            // Generate random genes
            for (let g = 0; g < dnaSize; g += geneSize) {
                this.dna.push(
                    Math.random(), // R
                    Math.random(), // G
                    Math.random(), // B
                    Math.max(Math.random() * Math.random(), 0.2) // A
                );
                const x = Math.random();
                const y = Math.random();
                for (let v = 0; v < numberOfVertices; v++) {
                    this.dna.push(
                        x + Math.random() - 0.5, // X
                        y + Math.random() - 0.5, // Y
                    );
                }
            }
        }
        this.evaluate();
    }

    evaluate() {
        this.draw(workingContext, internalResolution);
        const workingData = workingContext.getImageData(0, 0, internalResolution, internalResolution).data;
        let error = 0;
        for (let i = 0; i < pixelDataSize; i++) {
            const pixelError = (workingData[i] - imageData[i]);
            error += pixelError * pixelError;
        }
        error = error / (pixelDataSize * 256 * 256);
        this.fitness = 1 - error;
    }

    draw(ctx, resolution) {
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, resolution, resolution);
        for (let g = 0; g < dnaSize; g += geneSize) {
            ctx.beginPath();
            ctx.moveTo(
                this.dna[g + 4] * resolution, 
                this.dna[g + 5] * resolution
            );
            for (let v = 0; v < numberOfVertices; v++) {
                ctx.lineTo(
                    this.dna[g + v * 2 + 6] * resolution,
                    this.dna[g + v * 2 + 7] * resolution
                );
            }
            ctx.closePath();

            ctx.fillStyle = `rgba(${(this.dna[g+0]*255) >> 0},${(this.dna[g+1]*255) >> 0},${(this.dna[g+2]*255) >> 0},${this.dna[g+3]})`;
            ctx.fill();
        }
    }
}

class Population {
    individuals = [];

    constructor() {
        for (let i = 0; i < populationSize; i++) {
            this.individuals.push(new Individual());
        }
    }

    iterate() {
        let offspring = [];
        const selectionCount = Math.floor(this.individuals.length * selectionCutoff);
        const offspringCount = Math.ceil(1 / selectionCutoff);
        this.individuals = this.individuals.sort(function(a, b) {
            return b.fitness - a.fitness;
        })
        for (let i = 0; i < selectionCount; i++) {
            for (let j = 0; j < offspringCount; j++) {
                let randomIndividualIndex = i;
                while (randomIndividualIndex == i) {
                    randomIndividualIndex = (Math.random() * selectionCount) >> 0;
                }
                const chosenIndividual = this.individuals[i];
                const randomIndividual = this.individuals[randomIndividualIndex];
                offspring.push(new Individual(chosenIndividual, randomIndividual));
            }
        }
        this.individuals = offspring;
    }

    getFittest() {
        return this.individuals.sort(function(a,b) {
            return b.fitness - a.fitness;
        })[0];
    }
}

function main() {
    workingContext.drawImage(image, 0, 0, displayResolution, displayResolution, 0, 0, internalResolution, internalResolution);
    imageData = workingContext.getImageData(0, 0, internalResolution, internalResolution).data;
    referenceContext.drawImage(image, 0, 0);

    population = new Population();
    window.requestAnimationFrame(loop);
}

function loop() {
    population.iterate();
    const fittest = population.getFittest();
    fittest.draw(outputContext, displayResolution);
    generation += 1;
    generationElement.innerHTML = generation;
    fitnessElement.innerHTML = fittest.fitness;
    window.requestAnimationFrame(loop);
}

const image = new Image();
image.onload = main
// function() {
//     referenceContext.drawImage(image, 0, 0);
//     const imageData = referenceContext.getImageData(0, 0, internalResolution, internalResolution);
//     // console.log(imageData);
// }
window.onload = function() {
    referenceCanvas = document.getElementById('referenceCanvas');
    referenceContext = referenceCanvas.getContext('2d');
    outputCanvas = document.getElementById('outputCanvas');
    outputContext = outputCanvas.getContext('2d');
    workingCanvas = document.getElementById('workingCanvas');
    workingContext = workingCanvas.getContext('2d');
    generationElement = document.getElementById('generation');
    fitnessElement = document.getElementById('fitness');

    setCanvasProperties(referenceCanvas, displayResolution);
    setCanvasProperties(outputCanvas, displayResolution);
    setCanvasProperties(workingCanvas, internalResolution);

    image.src = './images/monalisa.jpg';
}
