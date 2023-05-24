Date.prototype.addHours = function(h) {
    this.setTime(this.getTime() + (h*60*60*1000));
    return this;
  }

Number.prototype.fillZero = function(width){
    let n = String(this);//문자열 변환
    return n.length >= width ? n:new Array(width-n.length+1).join('0')+n;//남는 길이만큼 0으로 채움
}

const currentTime = new Date();
const currentYear = currentTime.getFullYear();
const currentMonth = currentTime.getMonth() + 1; // Months are zero-based
const currentDay = currentTime.getDate();
const currentHour = currentTime.getHours();

const predictTime = currentTime.addHours(3);
const predictYear = predictTime.getFullYear();
const predictMonth = predictTime.getMonth() + 1; // Months are zero-based
const predictDay = predictTime.getDate();
const predictHour = predictTime.getHours();

function showResult()
{
    document.getElementById("year").value = "{{ year }}";
    updateMonths("{{ year }}");
    document.getElementById("month").value = "{{ month }}";
    document.getElementById("day").value = "{{ day }}";
    document.getElementById("time").value = "{{ time }}";
}

function initHours()
{
    let select = document.getElementById("time");
    for (let i = 0; i <= 23; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.text = i.fillZero(2) + '시';
        if (i == currentHour)
            option.selected = true;
        select.appendChild(option);
    }
}

function initDays()
{
    let select = document.getElementById("day");
    for (let i = 1; i <= 31; i++)
    {
        let option = document.createElement("option");
        option.value = i;
        option.text = String(i) + '일';
        if (i == currentDay)
            option.selected = true;
        select.appendChild(option);
    }
}

function initYears()
{
    let select = document.getElementById("year");
    let start = predictYear - 1;
    let end = predictYear;
    for (let i = start; i <= end; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.text = String(i) + '년';
        if (i == currentYear)
        {
            console.log(currentYear);
            option.selected = true;
        }
        select.appendChild(option);
    }
    updateMonths(currentYear);
}

function updateMonths(year) {
    let select = document.getElementById("month");
    let start = 1;
    let end = 12;
    select.innerHTML = "";
    if (year == predictYear)
        end = predictMonth;
    else
        start = Math.abs(predictMonth - 12);
    for (let i = start; i <= end; i++) {
            let option = document.createElement("option");
            option.value = i;
            option.text = String(i) + '월';
            if (i == end)
                option.selected = true;
            select.appendChild(option);
        }
    updateDays();
}

function getLastDay(year, month)
{
    last = new Date(year, month, 0);
    return (last.getDate());
}

function updateDays() {
    let select = document.getElementById("day");
    const year = document.getElementById("year").value;
    const month = document.getElementById("month").value;
    const day = select.childNodes;
    let lastDay = getLastDay(year, month);
    if (month == predictMonth)
        lastDay = predictDay;
    for (let i = predictDay < 28 ? predictDay : 28 ; i < 31; i++)
        day[i].hidden = false;
    for (let i = lastDay; i < 31; i++)
        day[i].hidden = true;
    updateHours();
}

function updateHours() {
    let select = document.getElementById("time");
    const year = document.getElementById("year").value;
    const month = document.getElementById("month").value;
    const day = document.getElementById("day").value;
    if (year == predictYear && month == predictMonth && day == predictDay)
    {
        const time = select.childNodes;
        for (let i = 1; i < 24; i++)
            time[i].hidden = false;
        for (let i = predictHour; i < 24; i++)
            time[i].hidden = true;
    }
}

// Call the function to populate the months dropdown initially
initHours();
initDays();
initYears();