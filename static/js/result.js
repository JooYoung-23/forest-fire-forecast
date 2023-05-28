function putLayerOnMap(map, pathOfGeoJson) {
    var xhr = new XMLHttpRequest();

    xhr.open('GET', pathOfGeoJson, true);
    xhr.onload = function() {    
        if (xhr.status === 200) {
            var geojson = JSON.parse(xhr.responseText);

            var geojsonLayer = new google.maps.Data({
                style: function(feature) {
                    return {
                        strokeWeight: 1,
                        strokeOpacity: 1,
                        strokeColor: 'white',
                        fillOpacity: 0
                    };
                }
            });

            geojsonLayer.addGeoJson(geojson);

            geojsonLayer.addListener('click', function(event) {
				const feature = event.feature;
				const sggName = feature.getProperty('SGG_NM');
				const risk = feature.getProperty('risk');

				//document.getElementById('name').innerHTML = sggName;
				//document.getElementById('risk').innerHTML = risk;

				const infoBox = document.getElementById('intro');
				infoBox.style.display = 'block';
				window.location.href = '#intro';

				/*
                const resultImage = document.getElementById('image_result');
				const resultPath = '../static/DB/result/';
				resultImage.src = resultPath + date_dir + '/' + sggName + "/result.png";
				resultImage.alt = resultPath + date_dir + '/' + sggName +"/result.png";

				for (let i = 1; i <= 4; i++) {
					const prevButton = document.getElementById(`div${i}`).querySelector("#prevButton");
					const nextButton = document.getElementById(`div${i}`).querySelector("#nextButton");
					prevButton.onclick = function(){prevImage(sggName, `div${i}`, 4)};
					nextButton.onclick = function(){nextImage(sggName, `div${i}`, 4)};
					toggleImage(sggName, `div${i}`, 0);
				}
                */
			});

            geojsonLayer.setMap(map);
        } else {
            console.log('Failed to load Gangwon_regions file');
        }
    };

    xhr.send();
}

function selectInfo()
{
    let radioBtns = document.getElementsByName("radioButton");

    for (var i = 0; i < radioBtns.length; i++) {
        var icon = radioBtns[i].nextElementSibling;

        if (radioBtns[i].checked) {
            icon.classList.remove("unchecked");
            icon.classList.add("checked");
        } else {
            icon.classList.remove("checked");
            icon.classList.add("unchecked");
        }
    }
    showInfo();
}

function showInfo()
{
    let checked = document.querySelector('input[name="radioButton"]:checked');
    let img_info = document.getElementById('image_info');
    let src_path = "ERROR";
    let title = "ERROR IS OCCURED.";

    if (checked.value == "temp")
    {
        src_path = "../static/DB/weather/" + date_dir + '/' + checked.value + ".png"
        title = " 기상 요인: 기온"
    }
    else if (checked.value == "rainfall")
    {
        src_path = "../static/DB/weather/" + date_dir + '/' + checked.value + ".png"
        title = " 기상 요인: 강수량"
    }
    else if (checked.value == "humidity")
    {
        src_path = "../static/DB/weather/" + date_dir + '/' + checked.value + ".png"
        title = " 기상 요인: 습도"
    }
    else if (checked.value == "wind")
    {
        src_path = "../static/DB/weather/" + date_dir + '/' + checked.value + ".png"
        title = " 기상 요인: 풍속"
    }
    else if (checked.value == "slope")
    {
        src_path = "../static/DB/land/"  + checked.value + ".png"
        title = " 지형 요인: 기울기"
    }
    else if (checked.value == "landuse")
    {
        src_path = "../static/DB/human/"  + checked.value + ".png"
        title = " 인적 요인: 기온"
    }
    img_info.src = src_path;
    document.querySelector('#view_info .image_title').innerHTML = "<h3 class='major'>" + title + "</h3>"
}

showInfo();

/*function showDiv(divId) {
    var div = document.getElementById(divId);
    var radioValue = document.querySelector('input[name="radioButton"]:checked').value;
    
    // Hide all divs
    var allDivs = document.querySelectorAll('div[id^="div"]');
    for (var i = 0; i < allDivs.length; i++) {
        allDivs[i].classList.add("hidden");
    }
    
    // Show the selected div
    if (div && radioValue === divId.substring(3)) {
        div.classList.remove("hidden");
    }
    var radioBtns = document.getElementsByName("radioButton");

    for (var i = 0; i < radioBtns.length; i++) {
        var icon = radioBtns[i].nextElementSibling;

        if (radioBtns[i].checked) {
            icon.classList.remove("unchecked");
            icon.classList.add("checked");
        } else {
            icon.classList.remove("checked");
            icon.classList.add("unchecked");
        }
    }
}

function nextImage(sggName, divId, numImages) {
    var currentImageIndex = parseInt(getCurrentImageIndex(divId));
    var nextImageIndex = (currentImageIndex + 1) % numImages;
    toggleImage(sggName, divId, nextImageIndex);
}

function prevImage(sggName, divId, numImages) {
    var currentImageIndex = parseInt(getCurrentImageIndex(divId));
    var prevImageIndex = (currentImageIndex - 1 + numImages) % numImages;
    toggleImage(sggName, divId, prevImageIndex);
}

function getCurrentImageIndex(divId) {
    var div = document.getElementById(divId);
    var image = div.querySelector("img");
    var imageIndex = image.src.split("/")[7].split(".")[0];

    return imageIndex;
}

function getDir(divId, sggName)
{
    var path = "../static/DB";
    var dir = "";
    if (divId == 'div1'){
        dir = path + "/result/" + date_dir + '/' +  sggName+ '/';
    }
    else if (divId == 'div2'){
        dir = path + "/weather/" + date_dir + '/' +  sggName+ '/';
    }
    else if (divId == 'div3'){
        dir = path + "/land/" + date_dir + '/' +  sggName+ '/';
    }
    else if (divId == 'div4'){
        dir = path + "/human/" + date_dir + '/' +  sggName+ '/';
    }
    return dir;
}

function toggleImage(sggName, divId, newIndex) {
    var div = document.getElementById(divId);
    var dir = getDir(divId, sggName);

    var image = div.querySelector("img");
    image.src = dir + newIndex.toString() + ".png";
    image.alt = dir + newIndex.toString() + ".png";
}*/