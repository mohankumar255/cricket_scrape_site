setInterval(setclock,1000)
const hourshand = document.querySelector('[data-hour-hand]')
const minuteshand = document.querySelector('[data-minute-hand]')
const secondshand = document.querySelector('[data-second-hand]')

function setclock(){

const current_date = new Date();
const seconds = current_date.getSeconds() /60
const minutes = (seconds+current_date.getMinutes())/60
const hours = (minutes+current_date.getHours())/12
setRotation(hourshand,hours)
setRotation(minuteshand,minutes)
setRotation(secondshand,seconds)

}

function setRotation(ele , rotationratio){
ele.style.setProperty('--rotation',rotationratio*360)
}

setclock()
