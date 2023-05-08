let box = document.getElementById("box");
let userAnswered = false
let lang = "ru"
let timerId
let allAttempt = 0
let goodAttempt = 0
let multiword = false

//[min, max)
function getRandomInt(min, max) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min) + min)
}

function shuffleArray(arr){
    //console.log(1010)
    console.log("debug mega: " +  arr.length)
    for(let i = 0; i < 30; i++){
        index1 = -1
        index2 = -1
        //console.log(345)
        //console.log(arr.length)
        while(index1 == index2){
            //console.log("debug: rere")
            index1 = getRandomInt(0, arr.length)
            index2 = getRandomInt(0, arr.length)
            console.log(index1 + " " + index2)
            
        }
        tmp = arr[index1]
        arr[index1] = arr[index2]
        arr[index2] = tmp
    }
    return arr
}

function updateCounter(){
    counter.innerText = "\t" + String(goodAttempt) + "/" + String(allAttempt)
}

function handleClick(event){
    if (userAnswered) return
    userAnswered = true
    let obj = event.currentTarget
    let counter = document.getElementById("counter")
    let labels = document.getElementsByTagName("label")
    let label
    for(let i = 0; i < labels.length; i++){
        if(labels[i].getAttribute("for") ==
           obj.getAttribute("id")){
               label = labels[i]
           }
    }
    allAttempt++;
    if(obj.getAttribute("value") == "true"){
        label.style.transition = "3s"
        label.style.backgroundColor = "#77c331"
        goodAttempt++
    } else {
        label.style.transition = "3s"
        label.style.backgroundColor = "#c7294a"
    }
    timerId = setTimeout(() => {generate()}, 2 * 1000);
}

function generate(){
    userAnswered = false
    box.innerHTML = ""
    updateCounter()
    let langFrom, langTo
    randWordIndex = getRandomInt(0, ru.length)
    if (lang == "ru") {
        if (!multiword) {
            langFrom = ru[randWordIndex]
            langTo = gr[randWordIndex]
        } else {
            langFrom = new Array()
            langTo = new Array()
            for(let i = 0; i < ru.length; i++){
                for(let k = 0; k < ru[i].length; k++){
                    langFrom.push(ru[i][k])
                    langTo.push(gr[i][k])
                }
            }
        }
    } else {
        if (!multiword){
            langFrom = gr[randWordIndex]
            langTo = ru[randWordIndex]
        } else {
            langFrom = new Array()
            langTo = new Array()
            for(let i = 0; i < ru.length; i++){
                for(let k = 0; k < ru[i].length; k++){
                    langTo.push(gr[i][k])
                    langFrom.push(ru[i][k])
                }
            }
        }
    }
    let minAnswers
    if (langFrom.length < 4) {
		minAnswers = langFrom.length
	} else {
		minAnswers = 4
	}
    let answersNumber = getRandomInt(minAnswers, langFrom.length)
    let goodAnswerIndex = getRandomInt(0, langFrom.length)
    let question = document.createElement("p")
    question.innerText = langFrom[goodAnswerIndex]
    box.append(question)
    //формируем массив ответов (индексы массива)
    let answers = new Array()
    answers.push(goodAnswerIndex)
    for (let i = 0; i < answersNumber-1; i++){
        let flag = false
        let randIndex = -1
        while(!flag){
            console.log("debug: 123")
            randIndex = getRandomInt(0, langFrom.length)
            flag = true
            for(let k = 0; k < answers.length; k++){
                if(answers[k]==randIndex){
                    flag = false
                }
            }
        }
        answers.push(randIndex)
    }
    // перемешиваем масив ответов
    answers = shuffleArray(answers)
    for (let i = 0; i < answersNumber; i++){
        let radio = document.createElement("input")
        radio.setAttribute("type", "radio")
        radio.setAttribute("name", "test")
        radio.setAttribute("value", "false")
        radio.setAttribute("id", i)
        radio.setAttribute("onChange", "handleClick(event)")
        if(answers[i] == goodAnswerIndex){
            radio.setAttribute("value", "true")
        }
        let label = document.createElement("label")
        label.setAttribute("for", i)
        label.innerText = langTo[answers[i]]
        box.appendChild(radio)
        box.appendChild(label)
        box.appendChild(document.createElement("br"))
        box.appendChild(document.createElement("br"))
    }
}

function changeLang(){
    clearTimeout(timerId)
    if (document.getElementById("select_ru").selected) {
        lang = "ru"
    } else {
        lang = "gr"
    }
    generate()
}

generate();
