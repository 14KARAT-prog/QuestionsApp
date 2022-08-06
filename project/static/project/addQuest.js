"use strict";

const addQuestBtn = document.getElementById('addQuest');


const addInputField = (addQuestBtn) => {
    let counter = 0;  // Счетчик для фиксирования добавлений полей
    if (addQuestBtn) {
        addQuestBtn.addEventListener('click', (e) => {
            if (counter < 3) {
                const btn = e.target;  // Нахожу кнопку
                let p = document.createElement('p');
                p.innerHTML = `
                    <label for="choice_${counter + 3}">Вариант ответа: </label>
                    <input class="form-control w-25 d-inline" id="choice_${counter + 3}" name="choice" autocomplete="off">
                    <button id="btn${counter}" class="btn btn-secondary btn-sm" type="button">Удалить</button>
                `
                btn.before(p); // Вставляю перед кнопкой


                const butt = document.getElementById(`btn${counter}`);  // Нахожу пноку "удалить"
                // Вешаю на нее клик который удаляет текущий <p> элемент
                butt.onclick = () => {
                    p.remove();
                    counter -= 1;
                }
    
                counter += 1;
            }
        })
    }
}

addInputField(addQuestBtn);