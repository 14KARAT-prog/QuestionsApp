"use strict";

const voteBtn = document.getElementById('vote-btn');  // нахожу нужную мне кнопку


const offDisableBtn = (voteBtn) => {
    // Проверяю есть ли кнопка
    if (voteBtn) {
        // Вешаю обработчик события клика на fieldset
        voteBtn.form.children[1].addEventListener('click', (e) => {
            if (e.target.localName === "input"){   // Проверяю что клик был по инпуту
                voteBtn.disabled = false;
            }
        })
    }
}

offDisableBtn(voteBtn);