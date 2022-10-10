/************** Canvas ***************/
var myCanvas = document.getElementById("myCanvas");
myCanvas.width =300;
myCanvas.height =300;
				
var ctx = myCanvas.getContext("2d"),
val;

var income = 100000;
var incomeDisplay = document.getElementById('income');
incomeDisplay.innerHTML = income

var foodDisplay = document.getElementById('foodRs');
var lifeDisplay = document.getElementById('lifeRs');
var rentDisplay = document.getElementById('rentRs');
var othersDisplay = document.getElementById('othersRs');
var savingDisplay = document.getElementById('savingRs');

//Display default vals


/************** Slider Variables ***************/
//Food
	var sliderFood = document.getElementById("food");
	var outputFood = document.getElementById("foodValue");
	outputFood.innerHTML = sliderFood.value; // Display the default slider value
    foodDisplay.innerHTML = income*sliderFood.value/100
	
	// Update the current slider value (each time you drag the slider handle)
	sliderFood.oninput = function() {
	outputFood.innerHTML = this.value;
    foodDisplay.innerHTML = income*this.value/100
	};
	
//Rent	
	var sliderRent = document.getElementById("rent");
	var outputRent = document.getElementById("rentValue");
	outputRent.innerHTML = sliderRent.value; // Display the default slider value
    rentDisplay.innerHTML = income*sliderRent.value/100
	
	// Update the current slider value (each time you drag the slider handle)
	sliderRent.oninput = function() {
	outputRent.innerHTML = this.value;
    rentDisplay.innerHTML = income*this.value/100
	};

//Lifestyle	
	var sliderLife = document.getElementById("life");
	var outputLife = document.getElementById("lifeValue");
	outputLife.innerHTML = sliderLife.value; // Display the default slider value
    lifeDisplay.innerHTML = income*sliderLife.value/100
	
	// Update the current slider value (each time you drag the slider handle)
	sliderLife.oninput = function() {
	outputLife.innerHTML = this.value;
    lifeDisplay.innerHTML = income*this.value/100
	};
	
//Others
	var sliderOthers = document.getElementById("others");
	var outputOthers = document.getElementById("othersValue");
	outputOthers.innerHTML = sliderOthers.value; // Display the default slider value
    othersDisplay.innerHTML = income*sliderOthers.value/100
	
	// Update the current slider value (each time you drag the slider handle)
	sliderOthers.oninput = function() {
		outputOthers.innerHTML = this.value;
        othersDisplay.innerHTML = income*this.value/100
	};
	

	
	

/************** Utility Functions ***************/	
function changeColoursData() {	
	 var categories = {
		"Food": parseInt(sliderFood.value),
		"Rent": parseInt(sliderRent.value),
		"Life": parseInt(sliderLife.value),
		"Others": parseInt(sliderOthers.value),
		"Saving": parseInt(100 - parseInt(sliderFood.value)- parseInt(sliderRent.value)- parseInt(sliderLife.value)- parseInt(sliderOthers.value))			
	};
    console.log('Im here', categories.Saving)
    if (categories.Saving<0){
        window.alert("Budget Overflow!!")
        return {
            "Food": 20,
            "Rent": 30,
            "Life": 10,
            "Others": 20,
            "Saving": 20			
        };
    }
	var outputSaving = document.getElementById("savingValue");
	outputSaving.innerHTML = categories.Saving;
    savingDisplay.innerHTML = income*categories.Saving/100
	return categories;
	
}
			
/* https://code.tutsplus.com/tutorials/how-to-draw-a-pie-chart-and-doughnut-chart-using-javascript-and-html5-canvas--cms-27197 */

function drawPieSlice(ctx,centerX, centerY, radius, startAngle, endAngle, color ){
		ctx.fillStyle = color;
		ctx.beginPath();
		ctx.moveTo(centerX,centerY);
		ctx.arc(centerX, centerY, radius, startAngle, endAngle);
		ctx.closePath();
		ctx.fill();
}

/************** Piechart Object ***************/
class Piechart {
    constructor(options) {
        this.options = options;
        this.canvas = options.canvas;
        this.ctx = this.canvas.getContext("2d");
        this.colors = options.colors;

        this.draw = function () {
            var total_value = 0;
            var color_index = 0;
            for (var categ in this.options.data) {
                val = this.options.data[categ];
                total_value += val;
            }

            var start_angle = 0;
            for (categ in this.options.data) {
                val = this.options.data[categ];
                var slice_angle = 2 * Math.PI * val / total_value;

                drawPieSlice(
                    this.ctx,
                    this.canvas.width / 2,
                    this.canvas.height / 2,
                    Math.min(this.canvas.width / 2, this.canvas.height / 2),
                    start_angle,
                    start_angle + slice_angle,
                    this.colors[color_index % this.colors.length]
                );

                start_angle += slice_angle;
                color_index++;
            }
        };

    }
}
				

/************** Initialize code and draw pie chart ***************/
function refreshPiechart(){
	var myPiechart = new Piechart(
	{
		canvas:myCanvas,
		data: changeColoursData(),
		colors: ["#FFAC28", "#0252AE", "#C1212E", "#1E384A", "#69B331"]
				//colours : food,rent,life,others,saving
	}
    
);
console.log('hi')
myPiechart.draw();
	
}

refreshPiechart();