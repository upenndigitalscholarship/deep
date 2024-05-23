
// fetch data for all records, item_data is an object that serves as a lookup ex. item_data[330]
let item_data;
let item_array;

fetch("../assets/data/item_data.json")
  .then(function (u) {
    return u.json();
  })
  .then(function (json) {
    item_data = json;
    // we also need an array of items for filtering
    item_array = Object.values(item_data);
    // convert all null values to empty strings
    item_array.forEach(item => {
      Object.keys(item).forEach(key => {
        if (item[key] === null) {
          item[key] = '';
        }
      });
    });

    // Place your code here that depends on the resolved fetch
  }).then(function (json) {
    search()
  }).catch(function (error) {
    console.error("Error fetching item data:", error);
  });


//listen for search_bar
let options = {
  valueNames: ['result_number', 'deep_id', 'item_title', 'authors_display', 'year', 'greg_full'],

  // Since there are no elements in the list, this will be used as template.
  item: function (values) {
    return `<tr id="${values.deep_id}" onclick="expand(this, ${values.deep_id});"><td class="result_number"><td class="deep_id"></td><td class="year"></td><td class="authors_display"></td><td class="item_title services title">${values.item_title}</td><td>Expand</td></tr>`
  }
};
let table = new List('users', options, []);


// temporary until groupBy is added to JS
let groupBy = function (xs, key) {
  return xs.reduce(function (rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;

  }, {});
};



// In the search interface, there are three types of input field. Some are text entry search field. These allow filtering 
// based on string matching.  Date fields allow the entry of a four-digit start and end year number. Choice fields
// allow search and selection from a dropdown of valid choices.
let search_fields = ['deep-id', 'title', 'title-page-modern', 'errata', 'title-page-old', 'argument', 'toreader', 'charachter-list', 'commendatory-verses', 'explicit', 'dedication', 'other-paratexts', 'actor-list', 'authororial-status', 'greg_number', 'stc_or_wing', 'brit-drama-number']

let date_fields = ['first-production', 'first-edition', 'year-published', 'date-first-performance-brit-filter']

let choice_fields = ['book_edition', 'play_edition', 'imprintlocation', 'stationer', 'printer', 'publisher', 'bookseller', 'latinontitle', 'paratextual', 'company_first-performance-brit-filter', 'title-page-author', 'illustration', 'author', 'authorial-status', 'company-first-performance', 'company', 'theater', 'playtype', 'genre', 'genreplaybook', 'blackletter', 'format', 'genre-brit-filter', 'author_paratext']



const update_searchSelect = (searchSelect, or = false) => {

  let filter = searchSelect.value
  let searchField = document.getElementById(searchSelect.id.replace('searchSelect', 'advancedSearchField'))
  // clear existing input in search field
  searchField.value = '';
  this_years = document.getElementById(searchSelect.id.replace('searchSelect', 'date-input'))
  this_years.classList.add('invisible')

  //reset result count, clear table
  rC = document.getElementById("resultCount")
  rC.innerText = ''
  table.clear();

  // Choice.js changes the <select> to a <div class="choices"> when initialized
  // when a div, it does not contain the id, so a sibling relation is used
  if (or) {
    choicesSelect = searchSelect.nextElementSibling.nextElementSibling
    searchSelect.dataset.name = filter
  } else {
    choicesSelect = searchSelect.parentElement.children[2]
    searchSelect.dataset.name = filter
  }
  // when switching between choice and search fields, then back, there is an issue
  // reconnecting with the choicefield. To avoid this issue, the choice element is 
  // removed and re-added, then re-initialized. It's kind of excessive, but necessisary 
  const newSelect = document.createElement("select");
  newSelect.id = choicesSelect.id
  newSelect.classList.add("form-control");
  newSelect.classList.add('invisible')
  choicesSelect.replaceWith(newSelect);

  newSelect.addEventListener('change', (event) => {
    search();
  })
  searchSelect.dataset.name = filter

  // search fields
  if (search_fields.indexOf(filter) > -1) {
    searchField.style.display = "block";
    this_years.classList.remove("d-none");

  }

  // date fields
  if (date_fields.indexOf(filter) > -1) {
    searchField.style.display = "none";
    this_years.classList.remove('invisible')
    choicesSelect.classList.add('d-none')
  }

  // choice fields
  if (choice_fields.indexOf(filter) > -1) {

    searchField.style.display = "none";
    newSelect.classList.remove('invisible')
    this_choices = new Choices(newSelect, {
      addItems: false,
      shouldSort: false,
      shouldSortItems: false,
      allowHTML: true,
      position: 'bottom',
      placeholder: 'Select an option',
    })
  }
  if (filter === 'title-page-author') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/title_page_author_filter.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'author_paratext') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/author_paratext.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);

  }
  if (filter === 'paratextual') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/paratextual.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'imprintlocation') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/locations.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'book_edition') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/book_editions.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'play_edition') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/play_editions.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'stationer') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/stationer.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'printer') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/printer.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'publisher') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/publisher.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'bookseller') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/bookseller.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'genre-brit-filter') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/genres_bd.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'company_first-performance-brit-filter') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/first-companies-brit.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'author') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/authors.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }

  if (filter === 'authorial-status') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/author_status.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }

  if (filter === 'illustration') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/yes-no.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'format') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/formats.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }

  if (filter === 'blackletter') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/yes-no.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'latinontitle') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/yes-no.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'genre') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/genre.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }

  if (filter === 'genreplaybook') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/genre_playbook.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'playtype') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/playtype.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);

  }
  if (filter === 'theater') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/theater.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'company-first-performance') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/first-companies.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
  if (filter === 'company') {
    this_choices.setChoices(async () => {
      try {
        const items = await fetch('/assets/data/title-page-companies.json');
        return items.json();

      } catch (err) {
        console.error(err);
      }
    },
      'value',
      'label',
      true);
  }
}

const noPunct = string => {
  return string.replace(/\,/g,"").replace(/\./g,"").replace(/\:/g,"").replace(/\;/g,"").replace(/\?/g,"").replace(/\-/g,"").replace(/\_/g,"")
}

const getQueries = () => {
  // for each block
  let query = []
  let blocks = document.getElementById('filterBlocks')
  for (let i = 0; i < blocks.children.length; i++) {
    let block = blocks.children[i]
    // get AND OR operator 
    let blockType = block.dataset.type

    if (blockType == 'AND') {
      let searchField = block.children[1].children[0].value

      // is a search field 
      if (search_fields.indexOf(searchField) > -1) {

        let searchValue = block.children[1].children[1].value

        if (searchValue) {
          query.push({ "searchField": searchField, "searchValue": searchValue, "blockType": blockType })
        } else {
          query.push({ "searchField": searchField, "searchValue": "[isblank]", "blockType": blockType })
        }
      }
      if (date_fields.indexOf(searchField) > -1) {
        // date field
        let start = block.children[1].children[5].children[1].value
        let end = block.children[1].children[5].children[3].value
        query.push({ "searchField": searchField, "searchValue": start + '-' + end, "blockType": blockType })
      }
      if (choice_fields.indexOf(searchField) > -1) {
        // choice field
        let searchValue = block.children[1].children[2].outerText.split('\n')[0] //TODO better way to access selected value
        if (searchValue) {
          query.push({ "searchField": searchField, "searchValue": searchValue, "blockType": blockType })
        }
      }

    }
    if (blockType == 'OR') {
      // first block
      let searchField1 = block.children[1].children[0].value

      if (search_fields.indexOf(searchField1) > -1) {
        searchValue1 = block.children[1].children[1].value
      }
      if (date_fields.indexOf(searchField1) > -1) {
        let start = block.children[1].children[5].children[1].value
        let end = block.children[1].children[5].children[3].value
        searchValue1 = start + '-' + end
      }
      if (choice_fields.indexOf(searchField1) > -1) {
        searchValue1 = block.children[1].children[2].outerText.split('\n')[0] //TODO better way to access selected value

      }
      // second block
      let searchField2 = block.children[1].children[7].value
      if (search_fields.indexOf(searchField2) > -1) {
        searchValue2 = block.children[1].children[8].value
      }
      if (date_fields.indexOf(searchField2) > -1) {
        let start = block.children[1].children[12].children[1].value
        let end = block.children[1].children[12].children[3].value
        searchValue2 = start + '-' + end
      }
      if (choice_fields.indexOf(searchField2) > -1) {
        searchValue2 = block.children[1].children[9].outerText.split('\n')[0] //TODO better way to access selected value
      }
      query.push({ "searchField": searchField1 + '||' + searchField2, "searchValue": searchValue1 + '||' + searchValue2, "blockType": blockType })

    }
  }
  console.log('is query', query)
  return query
}

function removeFilterBlock(id) {
  let myParent = document.getElementById(id);
  myParent.remove();
  search();

}



function addANDBlock() {
  const min_year = '1512'
  const max_year = '1661'
  selectID = Date.now()
  let template = `
    <div id="andORButtons" class="btn-group" style="visibility:collapse;" role="group">
        <!-- Add new filter box 
          The top box has option to add AND OR
          Each child has a disabled button with the operator selected, and a remove button
        -->
                  
        <input type="radio" class="btn-check" name="addAND" id="addAND" autocomplete="off" disabled >
          <label class="btn btn-sm" for="addAND">and</label>              
            <input type="radio" class="btn-check btn-outline-dark" name="removeBlock" id="removeBlock" autocomplete="off">
            <label class="btn btn-sm" for="removeBlock"><i id="removeFilterBlock" class="bi bi-dash-circle" ></i></label>
    </div>
    <div>
      <select id="searchSelect-${selectID}" class="input-group form-select form-select-sm">
        
        <option value="">Please select...</option>
        <option value="deep-id">DEEP #</option>
        <option value="brit-drama-number">BritDrama #</option>
        <option value="title" selected>Title</option>
        <option value="title-page-modern">All Title-Page Text (modern spelling)</option>
        <option value="title-page-old">All Title-Page Text (old spelling)</option>  
        <option value="author">Author (Modern)</option>
        <option value="title-page-author">Author (Title Page)</option>
        <option value="author_paratext">Author (Paratext)</option>
        <option value="authorial-status">Authorial Status (Title Page)</option>
        <option value="company-first-performance">Company of First Production (Annals)</option>
        <option value="company_first-performance-brit-filter">Company of First Production (BritDrama)</option>
        <option value="company">Company (Title Page)</option>
        <option value="theater">Theater (Title Page)</option>
        <option value="playtype">Play Type</option>
        <option value="genre">Genre (Annals)</option>
        <option value="genre-brit-filter">Genre (BritDrama)</option>
        <option value="genreplaybook" >Genre (Title Page)</option>
        <option value="paratextual" >Paratextual Material</option>
        <option value="illustration">Illustration</option>
        <option value="blackletter">Black Letter</option>
        <option value="latinontitle">Latin on Title Page</option>
        <option value="stationer">Stationer</option>
        <option value="printer" >&nbsp;&nbsp;&nbsp;&nbsp;Printer</option>
        <option value="publisher" >&nbsp;&nbsp;&nbsp;&nbsp;Publisher</option>
        <option value="bookseller" >&nbsp;&nbsp;&nbsp;&nbsp;Bookseller</option>
        <option value="imprintlocation">Imprint Location</option>
        <option value="first-production">Date of First Production (Annals)</option>
        <option value="date-first-performance-brit-filter">Date of First Production (BritDrama)</option>
        <option value="first-edition">Date of First Edition</option>
        <option value="format">Format</option>
        <option value="book_edition">Book edition number</option>
        <option value="play_edition">Play edition number</option>
        <option value="greg_number">Greg Number</option>
        <option value="stc_or_wing">STC / Wing Number</option>
        <option value="year-published">Year Published</option>

      </select>
      <input id="advancedSearchField-${selectID}" type="text" class="form-control" aria-label="advancedSearchField" aria-describedby="advancedSearchField">
      <select id="choicesSelect-${selectID}" style="display: hide;" class="form-control"></select>
        
      <style>.noUi-connect {
        background: #0e0076;
      }</style>
      <div id="spacer" style="height:10px;"></div>
      <div id="date-input-${selectID}" class="input-group d-none">
        <span class="input-group-text">Begin:</span>
        <input type="number" aria-label="start-date" placeholder="${min_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
        <span class="input-group-text">End:</span>
        <input type="number" aria-label="end-date" placeholder="${max_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
      </div></div>`


  let newBlock = document.createElement("div");
  newBlock.innerHTML = template

  //  Don't add 'and' or buttons to first block
  if (document.getElementById('filterBlocks').childElementCount === 0) {
    newBlock.children[0].style.display = "none";
  }

  document.getElementById('filterBlocks').append(newBlock);


  // Add a unique id to the new block and update as AND OR filter
  //let newBlock = document.getElementById('filterBlocks').lastElementChild
  newBlock.id = 'filterBlock-' + document.getElementById('filterBlocks').childElementCount
  // <div id="filterBlock" class="input-group-md">
  newBlock.classList.add("input-group-md");
  // listen for changes to searchSelect

  let searchSelect = newBlock.children[1].children[0]
  update_searchSelect(searchSelect);
  searchSelect.addEventListener('change', (event) => {
    update_searchSelect(searchSelect);
  })

  let thisSearchField = newBlock.children[1].children[1]
  thisSearchField.addEventListener('keyup', (event) => {
    search();
  });

  let thisChoicesSelect = newBlock.children[1].children[2]
  thisChoicesSelect.addEventListener('change', (event) => {
    search();
  });

  let beginDateSelect = newBlock.children[1].children[5].children[1]
  beginDateSelect.addEventListener('keyup', (event) => {
    search();
  });

  let endDateSelect = newBlock.children[1].children[5].children[3]
  endDateSelect.addEventListener('keyup', (event) => {
    search();
  });

  let typeName = newBlock.children[0].children[1];

  newBlock.dataset.type = "AND"
  typeName.innerHTML = 'and'

  typeName.style.visibility = 'visible';


  let removeButton = newBlock.children[0].children[3];
  removeButton.style.visibility = 'visible';
  removeButton.addEventListener('click', function handleClick(event) {
    removeFilterBlock('filterBlock-' + document.getElementById('filterBlocks').childElementCount);
  });
}

function addORBlock() {
  const min_year = '1512'
  const max_year = '1661'
  selectID1 = Date.now()
  selectID2 = Math.floor(Date.now() / 2)
  let template = `
    <div id="andORButtons" class="btn-group" role="group" aria-label="Basic radio toggle button group">          
        <input type="radio" class="btn-check" name="addAND" id="addAND" autocomplete="off" disabled >
          <label class="btn btn-sm  " for="addAND">and</label>              
            <input type="radio" class="btn-check btn-outline-dark" name="removeBlock" id="removeBlock" autocomplete="off">
            <label class="btn btn-sm" for="removeBlock"><i id="removeFilterBlock" class="bi bi-dash-circle" ></i></label>
    </div>
    <div class="border border-dark rounded border-2">
      <select id="searchSelect-${selectID1}" class="input-group form-select form-select-sm">
        
        <option value="">Please select...</option>
        <option value="deep-id">DEEP #</option>
        <option value="brit-drama-number">BritDrama #</option>
        <option value="title" selected>Title</option>
        <option value="title-page-modern">All Title-Page Text (modern spelling)</option>
        <option value="title-page-old">All Title-Page Text (old spelling)</option>  
        <option value="author">Author (Modern)</option>
        <option value="title-page-author">Author (Title Page)</option>
        <option value="author_paratext">Author (Paratext)</option>
        <option value="authorial-status">Authorial Status (Title Page)</option>
        <option value="company-first-performance">Company of First Production (Annals)</option>
        <option value="company_first-performance-brit-filter">Company of First Production (BritDrama)</option>
        <option value="company">Company (Title Page)</option>
        <option value="theater">Theater (Title Page)</option>
        <option value="playtype">Play Type</option>
        <option value="genre">Genre (Annals)</option>
        <option value="genre-brit-filter">Genre (BritDrama)</option>
        <option value="genreplaybook" >Genre (Title Page)</option>
        <option value="paratextual" >Paratextual Material</option>
        <option value="illustration">Illustration</option>
        <option value="blackletter">Black Letter</option>
        <option value="latinontitle">Latin on Title Page</option>
        <option value="stationer">Stationer</option>
        <option value="printer" >&nbsp;&nbsp;&nbsp;&nbsp;Printer</option>
        <option value="publisher" >&nbsp;&nbsp;&nbsp;&nbsp;Publisher</option>
        <option value="bookseller" >&nbsp;&nbsp;&nbsp;&nbsp;Bookseller</option>
        <option value="imprintlocation">Imprint Location</option>
        <option value="first-production">Date of First Production (Annals)</option>
        <option value="date-first-performance-brit-filter">Date of First Production (BritDrama)</option>
        <option value="first-edition">Date of First Edition</option>
        <option value="format">Format</option>
        <option value="book_edition">Book edition number</option>
        <option value="play_edition">Play edition number</option>
        <option value="greg_number">Greg Number</option>
        <option value="stc_or_wing">STC / Wing Number</option>
        <option value="year-published">Year Published</option>
        
      </select>
      <input id="advancedSearchField-${selectID1}" type="text" class="form-control" aria-label="advancedSearchField" aria-describedby="advancedSearchField">
      <select id="choicesSelect-${selectID1}" style="display: hide;" class="form-control"></select>
        
      <style>.noUi-connect {
        background: #0e0076;
      }</style>
      <div id="spacer" style="height:10px;"></div>
      <div id="date-input-${selectID1}" class="input-group d-none">
        <span class="input-group-text">Begin:</span>
        <input type="number" aria-label="start-date" value="${min_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
        <span class="input-group-text">End:</span>
        <input type="number" aria-label="end-date" value="${max_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
      </div>
      
      <label class="btn btn-sm  " for="addAND">or</label> 
                 
      <select id="searchSelect-${selectID2}" class="input-group form-select form-select-sm">
        
        <option value="">Please select...</option>
        <option value="deep-id">DEEP #</option>
        <option value="brit-drama-number">BritDrama #</option>
        <option value="title" selected>Title</option>
        <option value="title-page-modern">All Title-Page Text (modern spelling)</option>
        <option value="title-page-old">All Title-Page Text (old spelling)</option>  
        <option value="author">Author (Modern)</option>
        <option value="title-page-author">Author (Title Page)</option>
        <option value="author_paratext">Author (Paratext)</option>
        <option value="authorial-status">Authorial Status (Title Page)</option>
        <option value="company-first-performance">Company of First Production (Annals)</option>
        <option value="company_first-performance-brit-filter">Company of First Production (BritDrama)</option>
        <option value="company">Company (Title Page)</option>
        <option value="theater">Theater (Title Page)</option>
        <option value="playtype">Play Type</option>
        <option value="genre">Genre (Annals)</option>
        <option value="genre-brit-filter">Genre (BritDrama)</option>
        <option value="genreplaybook" >Genre (Title Page)</option>
        <option value="paratextual" >Paratextual Material</option>
        <option value="illustration">Illustration</option>
        <option value="blackletter">Black Letter</option>
        <option value="latinontitle">Latin on Title Page</option>
        <option value="stationer">Stationer</option>
        <option value="printer" >&nbsp;&nbsp;&nbsp;&nbsp;Printer</option>
        <option value="publisher" >&nbsp;&nbsp;&nbsp;&nbsp;Publisher</option>
        <option value="bookseller" >&nbsp;&nbsp;&nbsp;&nbsp;Bookseller</option>
        <option value="imprintlocation">Imprint Location</option>
        <option value="first-production">Date of First Production (Annals)</option>
        <option value="date-first-performance-brit-filter">Date of First Production (BritDrama)</option>
        <option value="first-edition">Date of First Edition</option>
        <option value="format">Format</option>
        <option value="book_edition">Book edition number</option>
        <option value="play_edition">Play edition number</option>
        <option value="greg_number">Greg Number</option>
        <option value="stc_or_wing">STC / Wing Number</option>
        <option value="year-published">Year Published</option>
       
      </select>
      <input id="advancedSearchField-${selectID2}" type="text" class="form-control" aria-label="advancedSearchField" aria-describedby="advancedSearchField">
      <select id="choicesSelect-${selectID2}" style="display: hide;" class="form-control"></select>
        
      <style>.noUi-connect {
        background: #0e0076;
      }</style>
      <div id="spacer" style="height:10px;"></div>
      <div id="date-input-${selectID2}" class="input-group d-none">
        <span class="input-group-text">Begin:</span>
        <input type="number" aria-label="start-date" value="${min_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
        <span class="input-group-text">End:</span>
        <input type="number" aria-label="end-date" value="${max_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
      </div></div>`


  let newBlock = document.createElement("div");
  newBlock.innerHTML = template


  // on first click, add OR as first block, 
  if (document.getElementById('filterBlocks').childElementCount == 1 && document.getElementById('filterBlocks').children[0].dataset.type == 'AND') {
    document.getElementById('filterBlocks').children[0].remove()
    document.getElementById('filterBlocks').append(newBlock);
    newBlock.children[0].style.display = "none";

  } else {
    document.getElementById('filterBlocks').append(newBlock);
  }



  // Add a unique id to the new block and update as AND OR filter
  //let newBlock = document.getElementById('filterBlocks').lastElementChild
  newBlock.id = 'filterBlock-' + document.getElementById('filterBlocks').childElementCount
  // <div id="filterBlock" class="input-group-md">
  newBlock.dataset.type = "OR"


  // First input
  let searchSelect1 = newBlock.children[1].children[0]
  update_searchSelect(searchSelect1);
  searchSelect1.addEventListener('change', (event) => {
    console.log('Iam searchSelect1 id', searchSelect1)
    update_searchSelect(searchSelect1);
  })
  let thisSearchField1 = newBlock.children[1].children[1]
  thisSearchField1.addEventListener('keyup', (event) => {
    search();
  });

  let thisChoicesSelect1 = newBlock.children[1].children[2]
  thisChoicesSelect1.addEventListener('change', (event) => {
    search();
  });

  let beginDateSelect1 = newBlock.children[1].children[5].children[1]
  beginDateSelect1.addEventListener('keyup', (event) => {
    search();
  });

  let endDateSelect1 = newBlock.children[1].children[5].children[3]
  endDateSelect1.addEventListener('keyup', (event) => {
    search();
  });

  // Second input
  let searchSelect2 = newBlock.children[1].children[7]
  update_searchSelect(searchSelect2, or = true);
  searchSelect2.addEventListener('change', (event) => {
    update_searchSelect(searchSelect2, or = true);
  })

  let thisSearchField2 = newBlock.children[1].children[8]
  thisSearchField2.addEventListener('keyup', (event) => {
    search();
  });

  let thisChoicesSelect2 = newBlock.children[1].children[9]
  thisChoicesSelect2.addEventListener('change', (event) => {
    search();
  });

  let beginDateSelect2 = newBlock.children[1].children[12].children[1]
  beginDateSelect2.addEventListener('keyup', (event) => {
    search();
  });

  let endDateSelect2 = newBlock.children[1].children[12].children[3]
  endDateSelect2.addEventListener('keyup', (event) => {
    search();
  });

  let removeButton = newBlock.children[0].children[3]
  removeButton.style.visibility = 'visible';
  removeButton.addEventListener('click', function handleClick(event) {
    removeFilterBlock(newBlock.id);
  });
}


function readFilterBlocks() {
  filterBlocks = document.getElementById('filterBlocks')
  for (i in filterBlocks.children) {
    let child = filterBlocks.children[i]
    let type = child.dataset.type
  }
}

// initialize searchBlock on page load
const init_firstBlock = () => {
  addANDBlock()
  let filterBlock = document.getElementById("filterBlock-1");
  searchSelect = filterBlock.children[1].children[0]
  update_searchSelect(searchSelect);
  searchSelect.addEventListener('change', (event) => {
    update_searchSelect(searchSelect);

  })
  const get_deep_id = window.location.pathname.replace(/\//g, '');
  
  if (get_deep_id) {
    // NOTE requires user to allow pop-up
    //window.open(`${deep_id}`);
    
    // set searchSelect to deep id
    searchSelect.value = 'deep-id';
    update_searchSelect(searchSelect);

    let searchField = document.getElementById(searchSelect.id.replace('searchSelect','advancedSearchField'));
    searchField.value = get_deep_id;
    // press enter 
    searchField.dispatchEvent(new KeyboardEvent('keyup',{'key':'Enter'}));
    // select expandAllButton
    setTimeout(function () { document.getElementById('expandAllButton').click(); }, 500);
    
    
  }
}
init_firstBlock();

const processQueries = queries => {

  const filters = []
  // https://stackoverflow.com/questions/67068405/dynamically-create-a-condition-in-javascript
  for (i in queries) {
    let query = queries[i]
    if (query.blockType == 'AND') {
      if (query.searchField == 'genreplaybook') {
        if (query.searchValue == "Any") {
          let genreplaybook = item => (
            item.title_page_genre != "None"
          )
          filters.push({ 'filter': genreplaybook, 'type': query.blockType })
        } else {
          let genreplaybook = item => (
            item.title_page_genre.split(';').map(s => s.trim()).indexOf(query.searchValue) > -1
          )
          filters.push({ 'filter': genreplaybook, 'type': query.blockType })
        }
      }
      if (query.searchField == 'author_paratext') {
        if (query.searchValue == "Any") {
          let authorParatext = item => (
            item.paratext_author != ""
          )
          filters.push({ 'filter': authorParatext, 'type': query.blockType })
        }
        else if (query.searchValue == "None") {
          let authorParatext = item => (
            item.paratext_author == ""
          )
          filters.push({ 'filter': authorParatext, 'type': query.blockType })
        }
        else {
          let authorParatext = item => (
            item.paratext_author.toLowerCase().includes(query.searchValue.toLowerCase())
          )
          filters.push({ 'filter': authorParatext, 'type': query.blockType })
        }
      }
      if (query.searchField == 'genre-brit-filter') {
        let genreBrit = item => (
          item.genre_brit_filter.toLowerCase().split(';').map(s => s.trim()).indexOf(query.searchValue.toLowerCase()) > -1 
        )
        filters.push({ 'filter': genreBrit, 'type': query.blockType })
      }
      if (query.searchField == 'title') {
        if (query.searchValue == "[isblank]") {
          let title = item => (
            item.item_title != ""
          )
          filters.push({ 'filter': title, 'type': query.blockType })
        } else {
          let title = (item) => {
            let tokens = noPunct(query.searchValue).toLowerCase().split(" ");
            let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
            let re = new RegExp(pattern, 'i');
            let match = noPunct(item.item_title + ' ' + item.item_alternative_keywords).match(re);

            return match !== null && match.length > 0;
          }
          filters.push({ 'filter': title, 'type': query.blockType })
        }

      }
      if (query.searchField == 'stationer') {
        let stationer = item => (
          item.stationer_printer_filter.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.stationer_publisher_filter.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.stationer_bookseller_filter.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': stationer, 'type': query.blockType })
      }
      if (query.searchField == 'paratextual') {
        if (query.searchValue == 'Any') {
          let paratextual = item => (
            !item.paratext_dedication == "" ||
            !item.paratext_commendatory_verses == "" ||
            !item.paratext_to_the_reader == "" ||
            !item.paratext_argument == "" ||
            !item.paratext_actor_list == "" ||
            !item.paratext_charachter_list == "" ||
            !item.paratext_explicit == "" ||
            !item.paratext_errata == "" ||
            !item.paratext_other_paratexts == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'None') {
          let paratextual = item => (
            item.paratext_dedication == "" &&
            item.paratext_commendatory_verses == "" &&
            item.paratext_to_the_reader == "" &&
            item.paratext_argument == "" &&
            item.paratext_actor_list == "" &&
            item.paratext_charachter_list == "" &&
            item.paratext_explicit == "" &&
            item.paratext_errata == "" &&
            item.paratext_other_paratexts == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Dedication') {
          let paratextual = item => (
            !item.paratext_dedication == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Commendatory Verses') {
          let paratextual = item => (
            !item.paratext_commendatory_verses == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'To the Reader') {
          let paratextual = item => (
            !item.paratext_to_the_reader == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Argument') {
          let paratextual = item => (
            !item.paratext_argument == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Character List') {
          let paratextual = item => (
            !item.paratext_charachter_list == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Actor List') {
          let paratextual = item => (
            !item.paratext_actor_list == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Explicit') {
          let paratextual = item => (
            !item.paratext_explicit == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Errata') {
          let paratextual = item => (
            !item.paratext_errata == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
        else if (query.searchValue == 'Other Paratexts') {
          let paratextual = item => (
            !item.paratext_other_paratexts == ""
          )
          filters.push({ 'filter': paratextual, 'type': query.blockType })
        }
      }
      if (query.searchField == 'title-page-modern') {
        let titlePageModern = item => (
          item.title_page_modern_spelling.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': titlePageModern, 'type': query.blockType })
      }
      if (query.searchField == 'imprintlocation') {
        let imprintLocation = item => (
          item.stationer_imprint_location.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': imprintLocation, 'type': query.blockType })
      }
      if (query.searchField == 'title-page-old') {
        let titlePageOld = item => (
          item.title_page_title.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.title_page_author.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.title_page_performance.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.title_page_latin_motto.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.stationer_imprint_location.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': titlePageOld, 'type': query.blockType })
      }
      if (query.searchField == 'title-page-author') {
        if (query.searchValue == "Any") {
          let titlePageAuthor = item => (
            item.title_page_author_filter !== "None"
          )
          filters.push({ 'filter': titlePageAuthor, 'type': query.blockType })
        } else if (query.searchValue == "None") {
          let titlePageAuthor = item => (
            item.title_page_author_filter == "None"
          )
          filters.push({ 'filter': titlePageAuthor, 'type': query.blockType })
        } else {
          let titlePageAuthor = item => (
            item.title_page_author_filter.split(';').map(s => s.trim()).indexOf(query.searchValue) > -1
          )
          filters.push({ 'filter': titlePageAuthor, 'type': query.blockType })
        }
      }

      if (query.searchField == 'illustration') {
        if (query.searchValue == "Yes") {
          let illustration = item => (
            item.title_page_illustration !== ""
          )
          filters.push({ 'filter': illustration, 'type': query.blockType })
        }
        else if (query.searchValue == "No") {
          let illustration = item => (
            item.title_page_illustration === ""
          )
          filters.push({ 'filter': illustration, 'type': query.blockType })
        }
      }
      if (query.searchField == 'latinontitle') {
        let latinontitle = item => (
          item.title_page_has_latin.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': latinontitle, 'type': query.blockType })

      }
      if (query.searchField == 'deep-id') {
        let deepID = (item) => {
          let pattern = `^${query.searchValue}$`;
          let re = new RegExp(pattern, 'i');
          let match = item.deep_id.match(re);

          return match !== null && match.length > 0;
        };
        filters.push({ 'filter': deepID, 'type': query.blockType })
      }
      if (query.searchField == 'greg_number') {
        let gregNumber = (item) => {
          // search item.greg_full for values[i]
          let pattern = `^${query.searchValue}$`;
          let re = new RegExp(pattern, 'i');
          let full_match = item.greg_full.match(re);
          let medium_match = item.greg_middle.match(re);
          let short_match = item.greg.match(re);
          if (full_match !== null && full_match.length > 0) {
            return true
          }
          else if (medium_match !== null && medium_match.length > 0) {
            return true
          }
          else if (short_match !== null && short_match.length > 0) {
            return true
          }

        };
        filters.push({ 'filter': gregNumber, 'type': query.blockType })
      }
      if (query.searchField == 'book_edition') {
        if (query.searchValue == "First") {
          let bookEdition = item => (
            item.book_edition == '1'
          )
          filters.push({ 'filter': bookEdition, 'type': query.blockType })
        } else if (query.searchValue == "Second-plus") {
          let bookEdition = item => (
            parseInt(item.book_edition) >= parseInt('2')
          )
          filters.push({ 'filter': bookEdition, 'type': query.blockType })
        } else {
          let bookEdition = item => (
            item.book_edition == query.searchValue
          )
          filters.push({ 'filter': bookEdition, 'type': query.blockType })
        }

      }
      if (query.searchField == 'play_edition') {
        if (query.searchValue == "First") {
          let bookEdition = item => (
            item.play_edition == '1'
          )
          filters.push({ 'filter': bookEdition, 'type': query.blockType })
        } else if (query.searchValue == "Second-plus") {
          let bookEdition = item => (
            parseInt(item.play_edition) >= parseInt('2')
          )
          filters.push({ 'filter': bookEdition, 'type': query.blockType })
        } else {
          let bookEdition = item => (
            item.play_edition == query.searchValue
          )
          filters.push({ 'filter': bookEdition, 'type': query.blockType })
        }
      }
      if (query.searchField == 'stc_or_wing') {
        let stcWing = (item) => {
          if (query.searchValue.includes(';')) {
            let tokens = query.searchValue.split(";");
            let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
            let re = new RegExp(pattern, 'i');
            let match = item.stc.match(re);
  
            return match !== null && match.length > 0;
          } else {
            let tokens = query.searchValue.split(" ");
            let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
            let re = new RegExp(pattern, 'i');
            let match = item.stc.match(re);
  
            return match !== null && match.length > 0;
          }
          
        };
        filters.push({ 'filter': stcWing, 'type': query.blockType })
      }
      if (query.searchField == 'author') {

        let author = item => (
          item.author.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': author, 'type': query.blockType })
      }
      if (query.searchField == 'authorial-status') {
        if (query.searchValue == 'Any') {
          let authorialStatus = item => (
            item.author_status != "None"
          )
          filters.push({ 'filter': authorialStatus, 'type': query.blockType })
        } else {
          let authorialStatus = item => (
            item.author_status.split(';').indexOf(query.searchValue) > -1
          )
          filters.push({ 'filter': authorialStatus, 'type': query.blockType })
        }
      }
      if (query.searchField == 'blackletter') {
        if (query.searchValue == "Yes" || query.searchValue == "Yes, Partly") {
          let blackletter = item => (
            item.blackletter.toLowerCase().includes("yes")
          )
          filters.push({ 'filter': blackletter, 'type': query.blockType })
        }
        if (query.searchValue == "No") {
          let blackletter = item => (
            item.blackletter.toLowerCase().includes(query.searchValue.toLowerCase())
          )
          filters.push({ 'filter': blackletter, 'type': query.blockType })
        }
      }
      if (query.searchField == 'genre') {
        let genre = item => (
          item.genre_annals_filter.split(';').indexOf(query.searchValue) > -1
        )
        filters.push({ 'filter': genre, 'type': query.blockType })
      }
      if (query.searchField == 'format') {
        let format = item => (
          item.format.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': format, 'type': query.blockType })
      }
      if (query.searchField == 'playtype') {
        let playtype = item => (
          item.play_type_filter.split(';').indexOf(query.searchValue) > -1
        )
        filters.push({ 'filter': playtype, 'type': query.blockType })
      }
      if (query.searchField == 'company') {
        if (query.searchValue == "Any") {
          let company = item => (
            item.title_page_company_filter !== "n/a" &&
            item.title_page_company_filter !== ""
          )
          filters.push({ 'filter': company, 'type': query.blockType })
        }
        else if (query.searchValue == "None") {
          let company = item => (
            item.title_page_company_filter == "" ||
            item.title_page_company_filter == "n/a"
          )
          filters.push({ 'filter': company, 'type': query.blockType })
        } else {
          let company = item => (
            item.title_page_company_filter.toLowerCase().includes(query.searchValue.toLowerCase())
          )
          filters.push({ 'filter': company, 'type': query.blockType })

        }
      }
      if (query.searchField == 'company-first-performance') {
        if (query.searchValue == "Any") {
          let companyFirstPerformance = item => (
            item.company_first_performance_annals_filter != "None"
          )
          filters.push({ 'filter': companyFirstPerformance, 'type': query.blockType })
        } else {
          let companyFirstPerformance = item => (
            item.company_first_performance_annals_filter.toLowerCase().includes(query.searchValue.toLowerCase())
          )
          filters.push({ 'filter': companyFirstPerformance, 'type': query.blockType })
        }
      }
      if (query.searchField == 'company_first-performance-brit-filter') {
        if (query.searchValue == "Any") {
          let companyFirstPerformanceBrit = item => (
            item.company_first_performance_brit_filter != "None"
          )
          filters.push({ 'filter': companyFirstPerformanceBrit, 'type': query.blockType })
        } else {
          let companyFirstPerformanceBrit = item => (
            item.company_first_performance_brit_filter.toLowerCase().includes(query.searchValue.toLowerCase())
          )
          filters.push({ 'filter': companyFirstPerformanceBrit, 'type': query.blockType })
        }
      }
      if (query.searchField == 'printer') {
        let printer = item => (
          item.stationer_printer_filter.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': printer, 'type': query.blockType })
      }
      if (query.searchField == 'publisher') {
        let publisher = item => (
          item.stationer_publisher_filter.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': publisher, 'type': query.blockType })
      }
      if (query.searchField == 'bookseller') {
        let bookseller = item => (
          item.stationer_bookseller_filter.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({ 'filter': bookseller, 'type': query.blockType })
      }
      if (query.searchField == 'brit-drama-number') {
        let britDrama = (item) => {
          if (query.searchValue.includes(';')) {
            let tokens = query.searchValue.split(";");
            let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
            let re = new RegExp(pattern, 'i');
            let match = item.brit_drama_number.match(re);
  
            return match !== null && match.length > 0;
          } else {
            let tokens = query.searchValue.split(" ");
            let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
            let re = new RegExp(pattern, 'i');
            let match = item.brit_drama_number.match(re);
  
            return match !== null && match.length > 0;
          }
          
        };
        filters.push({ 'filter': britDrama, 'type': query.blockType })
      }

      if (query.searchField == 'theater') {
        if (query.searchValue == "Indoor Professional") {
          let theater_filter = item => (
            item.theater_type == "Indoor" ||
            item.theater_type == "Both Indoor and Outdoor"
          )
          filters.push({ 'filter': theater_filter, 'type': query.blockType })
        }
        else if (query.searchValue == "Outdoor Professional") {
          let theater_filter = item => (
            item.theater_type == "Outdoor" ||
            item.theater_type == "Both Indoor and Outdoor"
          )
          filters.push({ 'filter': theater_filter, 'type': query.blockType })
        }
        else if (query.searchValue == "Any") {
          let theater_filter = item => (
            item.theater != "None" ||
            item.theater_type != "None"
          )
          filters.push({ 'filter': theater_filter, 'type': query.blockType })
        }
        else if (query.searchValue == "None") {
          let theater_filter = item => (
            item.theater == "None"
          )
          filters.push({ 'filter': theater_filter, 'type': query.blockType })
        } else {
          console.log('I am theater searchValue', query.searchValue);
          let theater_filter = item => (
            item.theater.split(';').indexOf(query.searchValue) > -1
          )
          filters.push({ 'filter': theater_filter, 'type': query.blockType })
        }
      }


      if (query.searchField == 'year-published') {
        let [start, end] = query.searchValue.split('-')
        let yearPublished = item => (
          item.year_int >= start && item.year_int <= end
        )
        filters.push({ 'filter': yearPublished, 'type': query.blockType })
      }
      if (query.searchField == 'first-production') {
        let [start, end] = query.searchValue.split('-')
        let firstProduction = item => (
          parseInt(item.date_first_performance_filter) >= parseInt(start) && parseInt(item.date_first_performance_filter) <= parseInt(end)
        )
        filters.push({ 'filter': firstProduction, 'type': query.blockType })
      }
      if (query.searchField == 'first-edition') {
        let [start, end] = query.searchValue.split('-')
        let firstEdition = item => (
          item.date_first_publication >= start && item.date_first_publication <= end
        )
        filters.push({ 'filter': firstEdition, 'type': query.blockType })
      }
      if (query.searchField == 'date-first-performance-brit-filter') {
        let [start, end] = query.searchValue.split('-')
        let firstPerformanceBrit = item => (
          parseInt(item.date_first_performance_brit_filter) >= parseInt(start) && parseInt(item.date_first_performance_brit_filter) <= parseInt(end)
        )
        filters.push({ 'filter': firstPerformanceBrit, 'type': query.blockType })
      }

    }
    //OR!
    if (query.blockType == 'OR') {
      // build two separate filters, then join them 
      let fields = query.searchField.split('||')
      let values = query.searchValue.split('||')
      let ORquery = []
      for (let i = 0; i < fields.length; i++) {
        if (fields[i] == 'title' && !values[i] == '') {
          let title = item => (
            item.item_title.toLowerCase().includes(values[i].toLowerCase()) ||
            item.title_alternative_keywords.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(title)
        }
        if (fields[i] == 'author_paratext' && !values[i] == '') {
          if (values[i] == 'Any') {
            let authorParatext = item => (
              item.paratext_author != ""
            )
            ORquery.push(authorParatext)
          }
          else if (values[i] == 'None') {
            let authorParatext = item => (
              item.paratext_author == ""
            )
            ORquery.push(authorParatext)
          } else {
            let authorParatext = item => (
              item.paratext_author.split(';').map(s => s.trim()).indexOf(values[i]) > -1
            )
            ORquery.push(authorParatext)
          }
        }
        if (fields[i] == 'genreplaybook' && values[i]) {
          if (values[i] == 'Any') {
            let genreplaybook = item => (
              item.title_page_genre != "None"
            )
            ORquery.push(genreplaybook)
          } else {
            let genreplaybook = item => (
              item.title_page_genre.split(';').map(s => s.trim()).indexOf(values[i]) > -1
            )
            ORquery.push(genreplaybook)
          }
        }
        if (fields[i] == 'genre-brit-filter' && values[i]) {
          let genreBrit = item => (
            item.genre_brit_filter.toLowerCase().split(';').map(s => s.trim()).indexOf(values[i].toLowerCase()) > -1 
          )
          ORquery.push(genreBrit)
        }
        if (fields[i] == 'stationer' && values[i]) {
          let stationer = item => (
            item.stationer_printer_filter.toLowerCase().includes(values[i].toLowerCase()) ||
            item.stationer_publisher_filter.toLowerCase().includes(values[i].toLowerCase()) ||
            item.stationer_bookseller_filter.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(stationer)
        }
        if (fields[i] == 'paratextual' && values[i]) {
          if (values[i] == 'Any') {
            let paratextual = item => (
              !item.paratext_dedication == "" ||
              !item.paratext_commendatory_verses == "" ||
              !item.paratext_to_the_reader == "" ||
              !item.paratext_argument == "" ||
              !item.paratext_actor_list == "" ||
              !item.paratext_charachter_list == "" ||
              !item.paratext_explicit == "" ||
              !item.paratext_errata == "" ||
              !item.paratext_other_paratexts == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'None') {
            let paratextual = item => (
              item.paratext_dedication == "" &&
              item.paratext_commendatory_verses == "" &&
              item.paratext_to_the_reader == "" &&
              item.paratext_argument == "" &&
              item.paratext_actor_list == "" &&
              item.paratext_charachter_list == "" &&
              item.paratext_explicit == "" &&
              item.paratext_errata == "" &&
              item.paratext_other_paratexts == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Dedication') {
            let paratextual = item => (
              !item.paratext_dedication == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Commendatory Verses') {
            let paratextual = item => (
              !item.paratext_commendatory_verses == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'To the Reader') {
            let paratextual = item => (
              !item.paratext_to_the_reader == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Argument') {
            let paratextual = item => (
              !item.paratext_argument == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Character List') {
            let paratextual = item => (
              !item.paratext_charachter_list == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Actor List') {
            let paratextual = item => (
              !item.paratext_actor_list == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Explicit') {
            let paratextual = item => (
              !item.paratext_explicit == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Errata') {
            let paratextual = item => (
              !item.paratext_errata == ""
            )
            ORquery.push(paratextual)
          }
          else if (values[i] == 'Other Paratexts') {
            let paratextual = item => (
              !item.paratext_other_paratexts == ""
            )
            ORquery.push(paratextual)
          }
        }
        // TODO There isn't an option for this, is that right?
        if (fields[i] == 'title-page-modern' && values[i]) {
          let titlePageModern = item => (
            item.title_page_modern_spelling.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(titlePageModern)
        }
        if (fields[i] == 'imprintlocation' && values[i]) {
          let imprintLocation = item => (
            item.stationer_imprint_location.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(imprintLocation)
        }
        if (fields[i] == 'title-page-old' && values[i]) {
          let titlePageOld = item => (
            item.title_page_title.toLowerCase().includes(values[i].toLowerCase()) ||
            item.title_page_author.toLowerCase().includes(values[i].toLowerCase()) ||
            item.title_page_performance.toLowerCase().includes(values[i].toLowerCase()) ||
            item.title_page_latin_motto.toLowerCase().includes(values[i].toLowerCase()) ||
            item.stationer_imprint_location.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(titlePageOld)
        }
        if (fields[i] == 'title-page-author' && values[i]) {
          if (values[i] == "Any") {
            let titlePageAuthor = item => (
              item.title_page_author_filter != "None"
            )
            ORquery.push(titlePageAuthor)
          } else if (values[i] == "None") {
            let titlePageAuthor = item => (
              item.title_page_author_filter == "None"
            )
            ORquery.push(titlePageAuthor)
          } else {
            let titlePageAuthor = item => (
              item.title_page_author_filter.split(';').map(s => s.trim()).indexOf(values[i]) > -1
            )
            ORquery.push(titlePageAuthor)
          }
        }
        if (fields[i] == 'brit-drama-number' && values[i]) {

          let britDrama = (item) => {
            if (values[i].includes(';')) {
              let tokens = values[i].split(";");
              let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
              let re = new RegExp(pattern, 'i');
              let match = item.brit_drama_number.match(re);
    
              return match !== null && match.length > 0;
            } else {
              let tokens = values[i].split(" ");
              let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
              let re = new RegExp(pattern, 'i');
              let match = item.brit_drama_number.match(re);
    
              return match !== null && match.length > 0;
            }
          };
          ORquery.push(britDrama)
        }
        if (fields[i] == 'illustration' && values[i]) {
          let illustration = item => (
            item.title_page_illustration.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(illustration)
        }
        if (fields[i] == 'latinontitle' && values[i]) {
          let latinontitle = item => (
            item.title_page_latin_motto.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(latinontitle)
        }
        if (fields[i] == 'deep-id' && values[i]) {
          let deepID = (item) => {
            let pattern = `^${values[i]}$`;
            let re = new RegExp(pattern, 'i');
            let match = item.deep_id.match(re);

            return match !== null && match.length > 0;
          };
          ORquery.push(deepID)
        }
        if (fields[i] == 'greg_number' && values[i]) {
          let gregNumber = (item) => {
            // search item.greg_full for values[i]
            let pattern = `^${values[i]}$`;
            let re = new RegExp(pattern, 'i');
            let full_match = item.greg_full.match(re);
            let medium_match = item.greg_middle.match(re);
            let short_match = item.greg.match(re);
            if (full_match !== null && full_match.length > 0) {
              return true
            }
            else if (medium_match !== null && medium_match.length > 0) {
              return true
            }
            else if (short_match !== null && short_match.length > 0) {
              return true
            }
          };
          ORquery.push(gregNumber)
        }
        if (fields[i] == 'book_edition' && values[i]) {
          if (values[i] == "First") {
            let bookEdition = item => (
              item.book_edition == '1'
            )
            ORquery.push(bookEdition)
          } else if (values[i] == "Second-plus") {
            let bookEdition = item => (
              parseInt(item.book_edition) >= parseInt('2')
            )
            ORquery.push(bookEdition)
          } else {
            let bookEdition = item => (
              item.book_edition == values[i]
            )
            ORquery.push(bookEdition)
          }
        }
        if (fields[i] == 'play_edition' && values[i]) {
          if (values[i] == "First") {
            let playEdition = item => (
              item.play_edition == '1'
            )
            ORquery.push(playEdition)
          } else if (values[i] == "Second-plus") {
            let playEdition = item => (
              parseInt(item.play_edition) >= parseInt('2')
            )
            ORquery.push(playEdition)
          } else {
            let playEdition = item => (
              item.play_edition == values[i]
            )
            ORquery.push(playEdition)
          }

        }
        if (fields[i] == 'stc_or_wing' && values[i]) {
          let stcWing = (item) => {
            if (values[i].includes(';')) {
              let tokens = values[i].split(";");
              let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
              let re = new RegExp(pattern, 'i');
              let match = item.stc.match(re);

              return match !== null && match.length > 0;
            } else {
              let tokens = values[i].split(" ");
              let pattern = tokens.map(token => `(?=.*\\b${token}\\b)`).join("");
              let re = new RegExp(pattern, 'i');
              let match = item.stc.match(re);

              return match !== null && match.length > 0;
            }
            
          };
          ORquery.push(stcWing)
        }
        if (fields[i] == 'author' && values[i]) {
          let author = item => (
            item.author.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(author)
        }
        if (fields[i] == 'authorial-status' && values[i]) {
          let authorialStatus = item => (
            item.author_status.split(';').indexOf(values[i]) > -1
          )
          ORquery.push(authorialStatus)
        }
        if (fields[i] == 'blackletter' && values[i]) {
          if (values[i] == "Yes") {
            let blackletter = item => (
              item.blackletter.toLowerCase().includes(values[i].toLowerCase())
            )
            ORquery.push(blackletter)
          }
          if (values[i] == "No") {
            let blackletter = item => (
              item.blackletter == "No"
            )
            ORquery.push(blackletter)
          }
        }
        if (fields[i] == 'genre' && values[i]) {
          let genre = item => (
            item.genre_annals_filter.split(';').indexOf(values[i]) > -1
          )
          ORquery.push(genre)
        }
        if (fields[i] == 'format' && values[i]) {
          let format = item => (
            item.format.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(format)
        }
        if (fields[i] == 'playtype' && values[i]) {
          let playtype = item => (
            item.play_type_filter.split(';').indexOf(values[i]) > -1
          )
          ORquery.push(playtype)
        }

        if (fields[i] == 'company' && values[i]) {

          if (values[i] == "Any") {
            let company = item => (
              item.title_page_company_filter != ""
            )
            ORquery.push(company)
          }
          if (values[i] == "None") {
            let company = item => (
              item.title_page_company_filter == "" ||
              item.title_page_company_filter == "n/a"
            )
            ORquery.push(company)
          } else {
            let company = item => (
              item.title_page_company_filter.toLowerCase().includes(values[i].toLowerCase())
            )
            ORquery.push(company)

          }
        }
        if (fields[i] == 'company-first-performance' && values[i]) {
          let companyFirstPerformance = item => (
            item.company_first_performance.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(companyFirstPerformance)
        }

        if (fields[i] == 'printer' && values[i]) {
          let printer = item => (
            item.stationer_printer.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(printer)
        }
        if (fields[i] == 'publisher' && values[i]) {
          let publisher = item => (
            item.stationer_publisher.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(publisher)
        }
        if (fields[i] == 'bookseller' && values[i]) {
          let bookseller = item => (
            item.stationer_bookseller.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(bookseller)
        }

        if (fields[i] == 'theater' && values[i]) {

          if (values[i] == "Indoor Professional") {
            let theater = item => (
              item.theater_type == "Indoor" ||
              item.theater_type == "Both Indoor and Outdoor"
            )
            ORquery.push(theater)
          }
          else if (values[i] == "Outdoor Professional") {
            let theater = item => (
              item.theater_type == "Outdoor" ||
              item.theater_type == "Both Indoor and Outdoor"
            )
            ORquery.push(theater)
          }
          else if (values[i] == "Any") {
            let theater = item => (
              item.theater != "None" ||
              item.theater_type != "None"
            )
            ORquery.push(theater)
          }
          else if (values[i] == "None") {
            let theater = item => (
              item.theater == "None" ||
              item.theater_type == "None"
            )
            ORquery.push(theater)
          } else {
            let theater = item => (
              item.theater.toLowerCase().includes(values[i].toLowerCase()) ||
              item.theater_type.toLowerCase().includes(values[i].toLowerCase())
            )
            ORquery.push(theater)

          }
        }
        if (fields[i] == 'year-published' && values[i]) {
          let [start, end] = values[i].split('-')
          let yearPublished = item => (
            item.year_int >= start && item.year_int <= end
          )
          ORquery.push(yearPublished)
        }
        if (fields[i] == 'first-production' && values[i]) {
          let [start, end] = values[i].split('-')
          let firstProduction = item => (
            parseInt(item.date_first_performance_filter) >= parseInt(start) && parseInt(item.date_first_performance_filter) <= parseInt(end)
          )
          ORquery.push(firstProduction)
        }
        if (fields[i] == 'date-first-performance-brit-filter' && values[i]) {
          let [start, end] = values[i].split('-')
          let firstPerformanceBrit = item => (
            parseInt(item.date_first_performance_brit_filter) >= parseInt(start) && parseInt(item.date_first_performance_brit_filter) <= parseInt(end)
          )
          ORquery.push(firstPerformanceBrit)
        }
        if (fields[i] == 'first-edition' && values[i]) {
          let [start, end] = values[i].split('-')
          let firstEdition = item => (
            item.date_first_publication >= start && item.date_first_publication <= end
          )
          ORquery.push(firstEdition)
        }
      }
      filters.push({ 'filter': ORquery, 'type': 'OR' })
    }
    let singlePlay = document.getElementById('singlePlay')
    if (!singlePlay.checked) {
      let singlePlayFilter = item => item.record_type != 'Single-Play Playbook'
      filters.push({ 'filter': singlePlayFilter, 'type': 'AND' })
    }
    let Collections = document.getElementById('Collections')
    if (!Collections.checked) {
      let collectionsFilter = item => item.record_type != 'Collection'
      filters.push({ 'filter': collectionsFilter, 'type': 'AND' })
    }
    let PlaysinCollections = document.getElementById('PlaysinCollections')
    if (!PlaysinCollections.checked) {
      let playsinCollections = item => item.record_type != 'Play in Collection'
      filters.push({ 'filter': playsinCollections, 'type': 'AND' })
    }
  }
  return filters
}


const search = () => {
  /* Filter the items and update results for each query block
   should have same results as comparable SQL query 
    case 1: Title("Hamlet") && Theater("Globe") && Theater("Swan") = None
    case 2: Title("Hamlet") && Theater("Globe") || Theater("Swan")
  */
  table.clear();
  types = []
  let queries = getQueries()
  let filters = processQueries(queries)

  // check if a type appears more than once
  // if not, then just chain filters and reduce
  // if yes, chain reduce, then join 


  // // 0 + 1 + 2 + 3 + 4
  // const initialValue = 0;
  // const sumWithInitial = item_data.reduce(
  //   (previousValue, currentValue) => previousValue + currentValue,
  //   initialValue
  // );
  let results = filters.reduce(
    (d, f) => {
      if (f.type == "AND") {
        // catch TypeError: d is undefined
        if (d == undefined) {
          console.log('[*] line 1893 filter undefined', d, f)
        } else {
          return d.filter(f.filter)
        }
      }
      if (f.type == "OR") {
        if (f.filter.length == 1) {
          return d.filter(f.filter[0])
        }
        if (f.filter.length == 2) {
          return d.filter(f.filter[0]).concat(d.filter(f.filter[1]))
        }
      }
    },
    item_array
  )
  if (results == undefined) {
    console.log('[*] line 1907 results undefined', results)
    results = []
  }
  // for (i in queries){
  //   let { filter, type } = processQuery(queries[i], results)
  //   if (type === 'AND') {
  //     // intersection (a ∩ b) of results and query result, elements common to both results and query result
  //     results = results.filter(function(e) { return result.indexOf(e) > -1; });
  //   }
  //   if (type === 'OR') {
  //     // union (a ∪ b) of results and query result, all elements in either results or query result
  //     results = [...new Set([...results, ...result])]
  //   }

  //}

  // logic for title-edition-record filtering 
  let filter = radioHelper();
  let grouped_results = []

  if (filter == 'title') {
    let groups = groupBy(results, 'title_id');

    for (i in groups) {
      if (groups[i].length == 1) {
        grouped_results.push(groups[i][0])
      } else {
        // sort the group by deep_id, return only lowest deep id
        let d = groups[i].sort((a, b) => a.deep_id - b.deep_id);
        grouped_results.push(d[0])
      }
    }
  } else if (filter == 'edition') {
    let groups = groupBy(results, 'title_id'); //TODO is this right? should either be title_id or edition_id
    for (i in groups) {
      if (groups[i].length == 1) {
        grouped_results.push(groups[i][0])
      } else {

        let play_editions = groupBy(groups[i], 'edition_id');
        for (p in play_editions) {
          if (play_editions[p].length == 1) {
            grouped_results.push(play_editions[p][0])
          } else {
            // sort edition group by deep_id, return lowest deep id
            let pe = play_editions[p].sort((a, b) => a.deep_id - b.deep_id);
            grouped_results.push(pe[0])
          }
        }
      }


    };
  } else if (filter == 'record') {
    grouped_results = results
  }
  // sort results by year, by deep if same year 
  grouped_results.sort(function (a, b) {
    return a.year_int - b.year_int || a.deep_id - b.deep_id;
  });
  for (i in grouped_results) {
    grouped_results[i].result_number = parseInt(i) + 1 + '.'
  }
  console.log('[*] results - grouped results ', grouped_results)
  resultCount = document.getElementById("resultCount")
  resultCount.innerText = grouped_results.length
  table.add(grouped_results);
  table.update();
  if (filter == 'title') {
    // hide DEEP # and Year columns when work is selected
    deepID = document.querySelector('[data-sort="deep_id"]')
    deepID.style.display = 'none'
    deepRows = document.querySelectorAll('.deep_id')
    deepRows.forEach(row => {
      row.style.display = 'none'
    })

    yearColumn = document.querySelector('[data-sort="year"]')
    yearColumn.style.display = 'none'
    yearRows = document.querySelectorAll('.year')
    yearRows.forEach(row => {
      row.style.display = 'none'
    })
  } else {
    deepID = document.querySelector('[data-sort="deep_id"]')
    deepID.style.display = 'table-cell'
    deepRows = document.querySelectorAll('.deep_id')
    deepRows.forEach(row => {
      row.style.display = 'table-cell'
    })

    yearColumn = document.querySelector('[data-sort="year"]')
    yearColumn.style.display = 'table-cell'
    yearRows = document.querySelectorAll('.year')
    yearRows.forEach(row => {
      row.style.display = 'table-cell'
    })
  }
}


// Section for record type filtering
const singlePlay = document.getElementById('singlePlay')
singlePlay.addEventListener('change', (event) => {
  let filterBlock = document.getElementById("filterBlock-1");
  searchSelect = filterBlock.children[1].children[0]
  let searchField = document.getElementById(searchSelect.id.replace('searchSelect', 'advancedSearchField'));
  // press enter
  if (searchField.value != '') {
    search();
  } else {
    searchField.dispatchEvent(new KeyboardEvent('keyup', { 'key': 'Space' }));
  }
});

const Collections = document.getElementById('Collections')
Collections.addEventListener('change', (event) => {
  let filterBlock = document.getElementById("filterBlock-1");
  searchSelect = filterBlock.children[1].children[0]
  let searchField = document.getElementById(searchSelect.id.replace('searchSelect', 'advancedSearchField'));
  // press enter
  if (searchField.value != '') {
    search();
  } else {
    searchField.dispatchEvent(new KeyboardEvent('keyup', { 'key': 'Space' }));
  }
});

const PlaysinCollections = document.getElementById('PlaysinCollections')
PlaysinCollections.addEventListener('change', (event) => {
  let filterBlock = document.getElementById("filterBlock-1");
  searchSelect = filterBlock.children[1].children[0]
  let searchField = document.getElementById(searchSelect.id.replace('searchSelect', 'advancedSearchField'));
  // press enter
  if (searchField.value != '') {
    search();
  } else {
    // press space
    searchField.dispatchEvent(new KeyboardEvent('keyup', { 'key': 'Space' }));
  }
});

const Works = document.getElementById('titleRadio')
Works.addEventListener('change', (event) => {
  search();
  setTimeout(function () { table.sort('author', { order: "asc" }); }, 500);
});

const Editions = document.getElementById('editionRadio')
Editions.addEventListener('change', (event) => {
  search();
});

// recordRadio
const Records = document.getElementById('recordRadio')
Records.addEventListener('change', (event) => {
  search();
});

function expand(e, deep_id) {
  let filter = radioHelper();
  // handle TypeError: item_data is undefined
  if (typeof item_data != 'undefined' && filter != 'title') {

    let data = item_data[e.id];
    console.log(data)
    e.outerHTML = `
  <tr id="${data.deep_id}" onclick="collapse(this, ${data.deep_id});"><td class="result_number">${e.children[0].innerText}</td><td class="deep_id">${data.deep_id}</td><td class="year">${data.year}</td><td class="authors_display">${data.authors_display}</td><td class="title">${data.item_title}</td><td>Collapse</td>
    <tr id="${data.deep_id}-exp">
    <td colspan="5">
      <div class="card" style="width: 100%;">
        
        <div class="card-body">
          <div class="row">
            <div class="col-5">
              <strong>Reference Information</strong>
            </div>
          </div>
          <div class="row">
          
            <div class="col-5">
              <p>
                ${!data.deep_id ? '' : '<span class="expand">DEEP #: </span><span id="deep_id"><a target="_blank" href="/' + data.deep_id + '">' + data.deep_id + '</a></span><br>'}
                ${!data.greg_full ? '' : '<span class="expand">Greg #: </span><span id="greg_full">' + data.greg_full + '</span><br>'}
                ${!data.stc ? '' : '<span class="expand">STC/WING #: </span><span id="stc"> ' + data.stc + '</span><br>'}
                ${'<span class="expand">BritDrama #: </span><span id="deep_id">' + data.brit_drama_number + '</span><br>'}
              </p>
              <p>
                ${!data.date_first_publication ? '' : '<span class="expand">Date of First Publication: </span><span id="date_first_publication">' + data.date_first_publication_display + '</span><br>'}
                ${!data.book_edition ? '' : '<span class="expand">Book Edition: </span><span id="book_edition"> ' + data.book_edition + '</span><br>'}
                ${!data.play_edition ? '' : '<span class="expand">Play Edition: </span><span id="play_edition"> ' + data.play_edition + '</span><br>'}
                ${!data.format ? '' : '<span class="expand">Format: </span><span id="format"> ' + data.format + '</span><br>'}
                ${!data.leaves ? '' : '<span class="expand">Leaves: </span><span id="leaves"> ' + data.leaves + '</span><br>'}
                ${!data.blackletter ? '' : '<span class="expand">Black Letter: </span><span id="blackletter"> ' + data.blackletter + '</span>'}
              </p>
            </div>    
            
            <div class="col-7">
              <p>
                ${!data.record_type ? '' : '<span class="expand">Record Type: </span><span id="record_type">' + data.record_type + '</span><br>'}
                ${!data.play_type_display ? '' : '<span class="expand">Play Type: </span><span id="play_type">' + data.play_type_display + '</span><br>'}
                ${!data.genre_annals_filter ? '' : '<span class="expand">Genre (Annals): </span><span id="genre">' + data.genre_annals_display + '</span><br>'}
                ${!data.genre_brit_display ? '' : '<span class="expand">Genre (BritDrama): </span><span id="genre">' + data.genre_brit_display + '</span><br>'}
              </p>
              <p>
                ${'<span class="expand">Date of First Production (Annals): </span><span id="date_first_performance">' + data.date_first_performance + '</span><br>'}
                ${'<span class="expand">Date of First Production (BritDrama): </span><span id="date_first_performance">' + data.date_first_performance_brit_display + '</span><br>'}
                ${'<span class="expand">Company of First Production (Annals): </span><span id="company_first_performance_annals_display">' + data.company_first_performance_annals_display + '</span><br>'}
                ${'<span class="expand">Company of First Production (BritDrama): </span><span id="company_first_performance">' + data.company_first_performance_brit_display + '</span><br>'}
                ${'<span class="expand">Company Attribution (Title-Page): </span><span id="title_page_company_display">' + data.title_page_company_display + '</span><br>'}
              </p>
            </div>

            <div class="col-12">
              <p>
                ${typeof data.total_editions === 'undefined' ? '' : '<br><span class="expand">Total Editions:</span><span id="total_editions"> ' + data.total_editions + '</span><br>'}
                ${data.variants === '' || data.variants === null ? '' : '<span class="expand"></span>'} 
                ${data.variants === '' || data.variants === null ? '' : '<br><span class="expand">Variants:</span><span id="variants"> ' + data.variants + ' ' + data.variant_link + '<br>'}
                ${data.collection_contains === '' || data.collection_contains === null ? '' : '<span class="expand"></span>'}
                ${data.collection_contains === '' ? '' : '<br><span class="expand">Collection Contains:</span><span id="collection_contains"> ' + data.collection_contains + '</span><br>'}
                ${data.in_collection === '' ? '' : '<br><span class="expand">In Collection:</span><span id="in_collection"> ' + data.in_collection + '</span><br>'}
                ${!data.independent_playbook ? '' : '<br><span class="expand">Also Appears as a Bibliographically Independent Playbook In </span><span id="independent_playbook"><a target="_blank" href="/' + data.independent_playbook_link_id + '">' + data.independent_playbook + '</a></span><br>'}
                ${!data.also_in_collection ? '' : '<br><span class="expand">Also Appears in Collection: </span><span id="also_in_collection">' + data.also_in_collection_link + '</span><br>'}
              </p>
            </div>    

          </div>  
         </div>
      </div>

      <div class="card" style="width: 100%; margin-top:2px;">
        <div class="card-body">
          <div class="row">
            <div class="col-12">
              <strong>Title-Page Features</strong>
              <p>
                ${!data.title_page_title ? '<span class="expand">Title: </span><span id="title_page_title"></span><br>' : '<div class="hanging"><span class="expand">Title: </span><span id="title_page_title">' + data.title_page_title + '</span></div>'}
                ${data.title_page_author == "None" ? '<span class="expand">Author: </span><span id="title_page_author"></span><br>' : '<span class="expand">Author: </span><span id="title_page_author">' + data.title_page_author + '</span><br>'}
                ${!data.title_page_performance ? '<span class="expand">Performance: </span><span id="title_page_performance"></span><br>' : '<div class="hanging"><span class="expand">Performance: </span><span id="title_page_performance">' + data.title_page_performance + '</span></div><br>'}
                ${!data.title_page_latin_motto ? '' : '<div class="hanging"><span class="expand">Latin Motto: </span><span id="title_page_latin_motto">' + data.title_page_latin_motto + '</span></div><br>'}
                ${!data.title_page_illustration ? '' : '<span class="expand">Illustration: </span><span id="title_page_illustration">' + data.title_page_illustration + '</span><br>'}
                ${!data.title_page_imprint ? '<span class="expand">Imprint: </span><span id="title_page_imprint"></span><br>' : '<div class="hanging"><span class="expand">Imprint: </span><span id="title_page_imprint">' + data.title_page_imprint + '</span></div><br>'}
                ${!data.title_page_colophon ? '' : '<div class="hanging"><span class="expand">Colophon: </span><span id="title_page_colophon">' + data.title_page_colophon + '</span></div><br>'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="card" style="width: 100%; margin-top:2px;">
        <div class="card-body">
          <div class="row">
            <div class="col-12">
              <strong>Paratextual Material</strong>
              <p>
                ${!data.paratext_dedication && !data.paratext_commendatory_verses && !data.paratext_explicit && !data.paratext_to_the_reader && !data.paratext_errata && !data.paratext_argument && !data.paratext_charachter_list && !data.paratext_actor_list && !data.paratext_other_paratexts ? 'None' : ""}
                ${!data.paratext_dedication ? '' : '<span class="expand">Dedication: </span><span id="paratext_dedication">' + data.paratext_dedication + '</span><br>'}
                ${!data.paratext_commendatory_verses ? '' : '<span class="expand">Commendatory Verses: </span><span id="paratext_commendatory_verses">' + data.paratext_commendatory_verses + '</span><br>'}
                ${!data.paratext_to_the_reader ? '' : '<span class="expand">To the Reader: </span><span id="paratext_to_the_reader">' + data.paratext_to_the_reader + '</span><br>'}
                ${!data.paratext_argument ? '' : '<span class="expand">Argument: </span><span id="paratext_argument">' + data.paratext_argument + '</span><br>'}
                ${!data.paratext_charachter_list ? '' : '<span class="expand">Character List: </span><span id="paratext_charachter_list">' + data.paratext_charachter_list + '</span><br>'}
                ${!data.paratext_actor_list ? '' : '<span class="expand">Actor List: </span><span id="paratext_actor_list">' + data.paratext_actor_list + '</span><br>'}
                ${!data.paratext_explicit ? '' : '<span class="expand">Explicit: </span><span id="paratext_explicit">' + data.paratext_explicit + '</span><br>'}
                ${!data.paratext_errata ? '' : '<span class="expand">Errata: </span><span id="paratext_errata">' + data.paratext_errata + '</span><br>'}
                ${!data.paratext_other_paratexts ? '' : '<span class="expand">Other Paratexts: </span><span id="paratext_other_paratexts">' + data.paratext_other_paratexts + '</span><br>'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="card" style="width: 100%; margin-top:2px;">
        <div class="card-body">
          <div class="row">
            <div class="col-12">
              <strong>Stationer Information</strong>
              <p>
                ${!data.stationer_colophon ? '' : '<div class="hanging"><span class="expand">Colophon: </span><span id="stationer_colophon">' + data.stationer_colophon + '</span></div><br>'}
                ${!data.stationer_printer_filter ? '' : '<span class="expand">Printer: </span><span id="stationer_printer">' + data.stationer_printer_display + '</span><br>'}
                ${!data.stationer_publisher_filter ? '' : '<span class="expand">Publisher: </span><span id="stationer_publisher">' + data.stationer_publisher_display + '</span><br>'}
                ${!data.stationer_bookseller_filter ? '' : '<span class="expand">Bookseller: </span><span id="stationer_bookseller">' + data.stationer_bookseller_display + '</span><br>'}
                ${data.stationer_imprint_location === "None" ? '' : '<span class="expand">Imprint Location: </span><span id="stationer_imprint_location">' + data.stationer_imprint_location + '</span><br>'}
                ${!data.stationer_license ? '' : '<span class="expand">License: </span><span id="stationer_license">' + data.stationer_license + '</span><br>'}
                ${"<div class='hanging'><span class='expand'>Entries in Stationers' Registers: </span><span id='stationer_entries_in_register'>" + data.stationer_entries_in_register + '</span></div><br>'}
                ${!data.stationer_additional_notes ? '' : '<span class="expand"></span>'} 
                ${!data.stationer_additional_notes ? '' : '<span class="expand">Additional Notes: </span><span id="stationer_additional_notes">' + data.stationer_additional_notes + '</span><br>'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </td>
    
  </tr>`;
  } else if (filter == 'title') {
    let data = item_data[e.id];
    let results = item_array.filter(item => item.title_id == data.title_id);
    let editions = []
    // get all items with the same greg as data.greg
    // TODO need to sort by edition !!! 
    if (results.length == 1) {
      editions.push(results[0])
    } else {
      let play_editions = groupBy(results, 'edition_id');
      for (p in play_editions) {
        if (play_editions[p].length == 1) {
          editions.push(play_editions[p][0])
        } else {
          // sort edition group by deep_id, return lowest deep id
          let pe = play_editions[p].sort((a, b) => a.deep_id - b.deep_id);
          editions.push(pe[0])
        }
      }
    }
    
    // order editions by item.year 
    editions.sort((a, b) => a.year_int - b.year_int);
    edition_links = editions.map(item => `<a target="_blank" href="/${item.deep_id}">${item.year} ${item.record_type}</a>`).join('<br>');

    console.log(data)
    e.outerHTML = `<tr id="${data.deep_id}" onclick="collapse(this, ${data.deep_id});"><td class="result_number">${e.children[0].innerText}</td><td class="authors_display">${data.authors_display}</td><td class="title">${data.item_title}</td><td>Collapse</td>
    <tr id="${data.deep_id}-exp">
    <td colspan="5">
      <div class="card" style="width: 100%;">
      
        <div class="card-body">
          <div class="row">
            <div class="col-5">
              ${edition_links}
            </div>
          </div>
        </div>
      </div>
  </td>`
  } else {
    console.log('[*] item_data undefined')
    // wait half a second then run search 
    setTimeout(function () { expand(e, deep_id); }, 500);
    search();
  }
}

// condition ? exprIfTrue : exprIfFalse
function collapse(e, deep_id) {

  let data = item_data[e.id];
  let filter = radioHelper();
  if (data) {
    if (filter == 'title') {
      e.outerHTML = `
        <tr id="${data.deep_id}" onclick="expand(this, ${data.deep_id});"><td class="result_number">${e.children[0].innerText}</td><td class="authors_display">${data.authors_display}</td><td class="title">${data.item_title}</td><td>Expand</td>`
      let expandCard = document.getElementById(e.id + '-exp');
      if (expandCard) {
        expandCard.remove();
      }
    } else {
      e.outerHTML = `
      <tr id="${data.deep_id}" onclick="expand(this, ${data.deep_id});"><td class="result_number">${e.children[0].innerText}</td><td class="deep_id">${data.deep_id}</td><td class="year">${data.year}</td><td class="authors_display">${data.authors_display}</td><td class="title">${data.item_title}</td><td>Expand</td>`
      let expandCard = document.getElementById(e.id + '-exp');
      if (expandCard) {
        expandCard.remove();
      }
    }
  }
}

function changeButtonCollapse() {
  let changeButton = document.getElementById('expandAllButton')
  changeButton.textContent = 'Collapse All';
  changeButton.setAttribute("onClick", "collapseAll(this)");
}


function expandAll(e) {
  e.textContent = 'Collapse All';
  e.setAttribute("onClick", "collapseAll(this)");
  let items = document.querySelectorAll('tr');
  items.forEach(function (item) {
    expand(item, item.id);
  });
}

function collapseAll(e) {
  e.textContent = 'Expand All';
  e.setAttribute("onClick", "expandAll(this)");
  let items = document.querySelectorAll('tr');
  items.forEach(function (item) {

    collapse(item, item.id);

  });

};

function radioHelper() {
  if (document.getElementById('titleRadio').checked) {
    return 'title';
  }
  else if (document.getElementById('editionRadio').checked) {
    return 'edition';
  }
  else if (document.getElementById('recordRadio').checked) {
    return 'record';
  }
}

// listen for radio filter changes

document.querySelectorAll('input[type=radio]').forEach(item => {
  item.addEventListener('change', event => {
    search();
  })
})


// keep the result numbers ascending even when columns are sorted
table.on('sortComplete', function (e, column, dir) {
  let items = document.querySelectorAll('tr');
  let i = 1;
  items.forEach(function (item) {
    if (!item.children[0].classList.contains('sort')) {
      item.children[0].innerText = i + '.';
      i++;
    }
  });
});

// keep the result numbers ascending even when expanding/collapsing
let reset_result_numbers = function () {
  let items = document.querySelectorAll('tr');
  let i = 1;
  items.forEach(function (item) {
    // do not update the header row or expanded rows
    if (!item.children[0].classList.contains('sort') || !item.id.includes('-exp')) {
      item.children[0].innerText = i + '.';
      i++;
    }
  });
}

