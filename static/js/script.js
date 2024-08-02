let mainContent = document.getElementsByClassName('main')[0].innerHTML;
let searchContent = document.getElementsByClassName('search')[0].innerHTML;
let isContentChanged = false;

function search() {
    let main = document.getElementsByClassName('main')[0];
    let search = document.getElementsByClassName('search')[0];
    if (isContentChanged) {
        main.innerHTML = mainContent;
        search.innerHTML = searchContent;
    } else {
        main.innerHTML = '<div class="info"><div class="search-title"><h1 class="search-title">Пошук</h1><h3 class="filters-btn" onclick="filters()">Фільтри</h3></div><form action="/search" method="POST" class="form"><input type="text" name="search" placeholder="Що вас цікавить?" class="search-input" autocomplete="off"><div class="filters"></div><input type="submit" value="Шукати" class="search-btn"></form></div></div>';

        search.innerHTML = '<span class="material-symbols-outlined f2">close</span>';
    }
    isContentChanged = !isContentChanged;
}



let isFilters = false;

function filters() {
    let filters = document.getElementsByClassName('filters')[0];
    if (isFilters) {
        filters.innerHTML = ''
    } else {
        filters.innerHTML = '<select name="city" class="user-data inps"><option value="Київ">Київ</option><option value="Харків">Харків</option><option value="Одеса">Одеса</option><option value="Дніпро">Дніпро</option><option value="Львів">Львів</option><option value="Запоріжжя">Запоріжжя</option><option value="Кривий Ріг">Кривий Ріг</option><option value="Миколаїв">Миколаїв</option><option value="Вінниця">Вінниця</option><option value="Херсон">Херсон</option><option value="Полтава">Полтава</option><option value="Чернігів">Чернігів</option><option value="Черкаси">Черкаси</option><option value="Суми">Суми</option><option value="Житомир">Житомир</option><option value="Хмельницький">Хмельницький</option><option value="Чернівці">Чернівці</option><option value="Тернопіль">Тернопіль</option><option value="Івано-Франківськ">Івано-Франківськ</option><option value="Луцьк">Луцьк</option><option value="Рівне">Рівне</option><option value="Ужгород">Ужгород</option></select>';
    }
    isFilters = !isFilters;
}



let mainContent2 = document.getElementsByClassName('main')[0].innerHTML;
let headerContent = document.getElementsByClassName('nav')[0].innerHTML;
let isCreated = false;

function create() {
    let main = document.getElementsByClassName('main')[0];
    let header = document.getElementsByClassName('nav')[0];
    if (isCreated) {
        main.innerHTML = mainContent2;
        header.innerHTML = headerContent;
    } else {
        main.innerHTML = '<div class="info"><h1 class="search-title">Нова звичка</h1><div class="search-cont"><div class="search-title"></div><form action="/new-habbit" method="POST" class="form"><input type="text" name="title" placeholder="Що за звичка?" class="search-input" autocomplete="off"><textarea class="search-input" name="description" rows="2" placeholder="Опишіть свою звичку.\nЯка її роль у вашому житті?"></textarea><input type="text" name="goal" placeholder="Мета у днях. Рекомендуємо 30 днів" class="search-input" autocomplete="off"><div class="filters"><select name="city" class="user-data inps"><option value="Київ">Київ</option><option value="Харків">Харків</option><option value="Одеса">Одеса</option><option value="Дніпро">Дніпро</option><option value="Львів">Львів</option><option value="Запоріжжя">Запоріжжя</option><option value="Кривий Ріг">Кривий Ріг</option><option value="Миколаїв">Миколаїв</option><option value="Вінниця">Вінниця</option><option value="Херсон">Херсон</option><option value="Полтава">Полтава</option><option value="Чернігів">Чернігів</option><option value="Черкаси">Черкаси</option><option value="Суми">Суми</option><option value="Житомир">Житомир</option><option value="Хмельницький">Хмельницький</option><option value="Чернівці">Чернівці</option><option value="Тернопіль">Тернопіль</option><option value="Івано-Франківськ">Івано-Франківськ</option><option value="Луцьк">Луцьк</option><option value="Рівне">Рівне</option><option value="Ужгород">Ужгород</option></select></div><input type="submit" value="Створити" class="search-btn"></form></div></div>';
        header.innerHTML = '<div class="nav-icon create" onclick="create(this)"><span class="material-symbols-outlined f2">close</span></div>';
    }
    isCreated = !isCreated;
}

function smoothScroll(target) {
    document.querySelector(target).scrollIntoView({ 
        behavior: 'smooth' 
    });
}