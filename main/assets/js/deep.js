
// fetch data for all records, item_data is an object that serves as a lookup ex. item_data[330]
let item_data;
let item_array;
fetch("../assets/data/item_data.json").then(
        function(u){ return u.json();}
      ).then(
        function(json){
          item_data = json;
          // we also need an array of items for filtering
          item_array = Object.values(item_data);
        });

//listen for search_bar
let options = {
      valueNames: ['deep_id','title', 'authors_display', 'year', 'greg_full' ],
      
      // Since there are no elements in the list, this will be used as template.
      item: function(values) { 
        return `<tr id="${values.id}" onclick="expand(this, ${values.id});"><td class="deep_id"></td><td class="year"></td><td class="authors_display"></td><td class="title"></td><td>Expand</td></tr>`
      }
    };
let table = new List('users', options, []);


// temporary until groupBy is added to JS
let groupBy = function(xs, key) {
  return xs.reduce(function(rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;

  }, {});
};



// In the search interface, there are three types of input field. Some are text entry search field. These allow filtering 
// based on string matching.  Date fields allow the entry of a four-digit start and end year number. Choice fields
// allow search and selection from a dropdown of valid choices.
let search_fields = ['deep-id','title','title-page-modern','errata','paratextual','title-page-old','title-page-author',
  'argument','latinontitle','toreader','imprintlocation','illustration','stationer','printer','publisher','bookseller',
  'charachter-list','commendatory-verses','explicit','dedication','other-paratexts','book_edition',
  'play_edition','actor-list','authororial-status','greg_number','stc_or_wing','brit-drama-number']

let date_fields = ['first-production','first-edition','year-published','date-first-performance-brit-filter']

let choice_fields = ['author','authorial-status','company-first-performance','company','theater','playtype','genre','genreplaybook','blackletter','format','genre-brit-filter','company-first-performance-brit-filter']

              

const update_searchSelect = (searchSelect, or=false) => {
    let filter = searchSelect.value
    searchField = searchSelect.nextElementSibling
    let this_years
    if (or) {
      this_years = searchSelect.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling
      this_years.classList.add('d-none')
    } else {
      this_years = searchSelect.parentElement.children[5]
      this_years.classList.add('d-none')
    }
    let choicesSelect;
    if (or) {
      choicesSelect = searchSelect.nextElementSibling.nextElementSibling
      searchSelect.dataset.name = filter
    } else {
      choicesSelect = searchSelect.parentElement.children[2]
      searchSelect.dataset.name = filter
    }

    // search fields
    
    if (search_fields.indexOf(filter) > -1) {
      
      searchField.style.display = "block";
      this_years.classList.add('d-none')
      choicesSelect.style.display = "none";
    }
    // date fields
    if (date_fields.indexOf(filter) > -1) {
      searchField.style.display = "none";
      this_years.classList.remove("d-none");
      choicesSelect.style.display = "none";
    }

    // choice fields
    
    if (filter === 'genre-brit-filter') { 
        this_choices = new Choices(choicesSelect,{
          addItems: false,
          shouldSort: false,
          shouldSortItems: false,
          allowHTML: true,
          position: 'bottom',
          placeholder: 'Select an option',
        }) 
        searchField.style.display = "none";
        this_years.classList.add('d-none')
        choicesSelect.style.display = "block";
        this_choices.init()
        this_choices.clearChoices()
        // change element to choices field
        this_choices.setChoices(async () => {
          try {
            const items = await fetch('/assets/data/genres_bd.json');
            return items.json();
            
        } catch (err) {
          console.error(err);
        }
        });
      }
    if (filter === 'author') { 
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      }) 
      searchField.style.display = "none";
      this_years.classList.add('d-none')
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/authors.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }
    if (filter === 'authorial-status') { 
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          //TODO why fetch json? just use item_data directly
          // get distinct author values from item_data
          const items = await fetch('/assets/data/author_status.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }
    if (filter === 'format') { 
      // hide advancedSearchField
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          //TODO why fetch json? just use item_data directly
          // get distinct author values from item_data
          const items = await fetch('/assets/data/formats.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }

    if (filter === 'blackletter') { 
      // hide advancedSearchField
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/blackletter.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }
    if (filter === 'genre') { 
      // hide advancedSearchField
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/genre.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }
    if (filter === 'genreplaybook') { 
      // hide advancedSearchField
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/genre_playbook.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }
    if (filter === 'playtype') {
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/playtype.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });

      
    }
    if (filter === 'theater') {
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/theater.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });
    }
    if (filter === 'company-first-performance') {
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/first-companies.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });

      
    }
    if (filter === 'company') {
      this_choices = new Choices(choicesSelect,{
        addItems: false,
        shouldSort: false,
        shouldSortItems: false,
        allowHTML: true,
        position: 'bottom',
        placeholder: 'Select an option',
      })
      searchField.style.display = "none";
      this_years.classList.add("d-none");
      choicesSelect.style.display = "block";
      this_choices.init()
      this_choices.clearChoices()
      // change element to choices field
      this_choices.setChoices(async () => {
        try {
          const items = await fetch('/assets/data/first-companies.json');
          return items.json();
          
      } catch (err) {
        console.error(err);
      }
      });

      
    }
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
          query.push({"searchField":searchField, "searchValue":searchValue, "blockType":blockType})
        }
      }
      if (date_fields.indexOf(searchField) > -1) {
        // date field
        let start = block.children[1].children[5].children[1].value
        let end = block.children[1].children[5].children[3].value
        query.push({"searchField":searchField, "searchValue":start+'-'+end, "blockType":blockType})
      }
      if (choice_fields.indexOf(searchField) > -1) {
        // choice field
        let searchValue = block.children[1].children[2].outerText.split('\n')[0] //TODO better way to access selected value
        if (searchValue){
          query.push({"searchField":searchField, "searchValue":searchValue, "blockType":blockType})
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
        searchValue1 = start+'-'+end
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
        searchValue2 = start+'-'+end
      }
      if (choice_fields.indexOf(searchField1) > -1) {
        searchValue2 = block.children[1].children[9].outerText.split('\n')[0] //TODO better way to access selected value
      } 
      query.push({"searchField":searchField1+'||'+searchField2, "searchValue":searchValue1+'||'+searchValue2, "blockType":blockType})
      
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
      <select id="searchSelect" class="input-group form-select form-select-sm">
        
        <option value="">Please select...</option>
        <option value="deep-id">DEEP ID</option>
        <option value="brit-drama-number">BritDrama #</option>
        <option value="title" selected>Title</option>
        <option value="title-page-modern">All Title-Page Text (modern spelling)</option>
        <option value="title-page-old">All Title-Page Text (old spelling)</option>  
        <option value="author">Author (Modern Attribution)</option>
        <option value="title-page-author">Author (Title-Page Attribution)</option>
        <option value="authorial-status">Authorial Status (Title-Page Attribution)</option>
        <option value="company-first-performance">Company (First Production)</option>
        <option value="company_first-performance-brit-filter">Company of First Performance (BritDrama)</option>
        <option value="company">Company (Title-Page Attribution)</option>
        <option value="theater">Theater (Title-Page Attribution)</option>
        <option value="playtype">Play Type</option>
        <option value="genre">Genre (Annals)</option>
        <option value="genre-brit-filter">Genre (BritDrama)</option>
        <option value="genreplaybook" >Genre (Title-Page Attribution)</option>
        <option value="paratextual" >All Paratextual Material</option>
        <option value="illustration">Illustration</option>
        <option value="blackletter">Black Letter</option>
        <option value="latinontitle">Latin on Title Page</option>
        <option value="stationer">Stationer</option>
        <option value="printer" >&nbsp;&nbsp;&nbsp;&nbsp;Printer</option>
        <option value="publisher" >&nbsp;&nbsp;&nbsp;&nbsp;Publisher</option>
        <option value="bookseller" >&nbsp;&nbsp;&nbsp;&nbsp;Bookseller</option>
        <option value="imprintlocation">Imprint Location</option>
        <option value="first-production">Date of First Production</option>
        <option value="date-first-performance-brit-filter">Date of First Performance (BritDrama)</option>
        <option value="first-edition">Date of First Edition</option>
        <option value="format">Format</option>
        <option value="book_edition">Book edition number</option>
        <option value="play_edition">Play edition number</option>
        <option value="greg_number">Greg Number</option>
        <option value="stc_or_wing">STC / Wing Number</option>
        <option value="year-published">Year Published</option>
        <option value="dedication">Dedication</option>
        <option value="toreader">To the Reader</option>
        <option value="argument">Argument</option>
        <option value="actor-list">Actor List</option>
        <option value="explicit">Explicit</option>
        <option value="errata">Errata</option>
        <option value="charachter-list">Character List</option>
        <option value="other-paratexts">Other Paratexts</option>
        <option value="commendatory-verses" >Commendatory Verses</option>

      </select>
      <input id="advancedSearchField" type="text" class="form-control" aria-label="advancedSearchField" aria-describedby="advancedSearchField">
      <select id="choicesSelect" style="display: hide;" class="form-control"></select>
        
      <style>.noUi-connect {
        background: #0e0076;
      }</style>
      <div id="spacer" style="height:10px;"></div>
      <div id="date-input" class="input-group d-none">
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
  newBlock.id = 'filterBlock-'+document.getElementById('filterBlocks').childElementCount
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
    removeFilterBlock('filterBlock-'+document.getElementById('filterBlocks').childElementCount);
  });
}

function addORBlock() {
    const min_year = '1512'
    const max_year = '1661'

  let template = `
    <div id="andORButtons" class="btn-group" role="group" aria-label="Basic radio toggle button group">          
        <input type="radio" class="btn-check" name="addAND" id="addAND" autocomplete="off" disabled >
          <label class="btn btn-sm  " for="addAND">and</label>              
            <input type="radio" class="btn-check btn-outline-dark" name="removeBlock" id="removeBlock" autocomplete="off">
            <label class="btn btn-sm" for="removeBlock"><i id="removeFilterBlock" class="bi bi-dash-circle" ></i></label>
    </div>
    <div class="border border-dark rounded border-2">
      <select id="searchSelect1" class="input-group form-select form-select-sm">
        
        <option value="">Please select...</option>
        <option value="deep-id">DEEP ID</option>
        <option value="brit-drama-number">BritDrama #</option>
        <option value="title" selected>Title</option>
        <option value="title-page-modern">All Title-Page Text (modern spelling)</option>
        <option value="title-page-old">All Title-Page Text (old spelling)</option>  
        <option value="author">Author (Modern Attribution)</option>
        <option value="title-page-author">Author (Title-Page Attribution)</option>
        <option value="authorial-status">Authorial Status (Title-Page Attribution)</option>
        <option value="company-first-performance">Company (First Production)</option>
        <option value="company_first-performance-brit-filter">Company of First Performance (BritDrama)</option>
        <option value="company">Company (Title-Page Attribution)</option>
        <option value="theater">Theater (Title-Page Attribution)</option>
        <option value="playtype">Play Type</option>
        <option value="genre">Genre (Annals)</option>
        <option value="genre-brit-filter">Genre (BritDrama)</option>
        <option value="genreplaybook" >Genre (Title-Page Attribution)</option>
        <option value="paratextual" >All Paratextual Material</option>
        <option value="illustration">Illustration</option>
        <option value="blackletter">Black Letter</option>
        <option value="latinontitle">Latin on Title Page</option>
        <option value="stationer">Stationer</option>
        <option value="printer" >&nbsp;&nbsp;&nbsp;&nbsp;Printer</option>
        <option value="publisher" >&nbsp;&nbsp;&nbsp;&nbsp;Publisher</option>
        <option value="bookseller" >&nbsp;&nbsp;&nbsp;&nbsp;Bookseller</option>
        <option value="imprintlocation">Imprint Location</option>
        <option value="first-production">Date of First Production</option>
        <option value="date-first-performance-brit-filter">Date of First Performance (BritDrama)</option>
        <option value="first-edition">Date of First Edition</option>
        <option value="format">Format</option>
        <option value="book_edition">Book edition number</option>
        <option value="play_edition">Play edition number</option>
        <option value="greg_number">Greg Number</option>
        <option value="stc_or_wing">STC / Wing Number</option>
        <option value="year-published">Year Published</option>
        <option value="dedication">Dedication</option>
        <option value="toreader">To the Reader</option>
        <option value="argument">Argument</option>
        <option value="actor-list">Actor List</option>
        <option value="explicit">Explicit</option>
        <option value="errata">Errata</option>
        <option value="charachter-list">Character List</option>
        <option value="other-paratexts">Other Paratexts</option>
        <option value="commendatory-verses" >Commendatory Verses</option>

      </select>
      <input id="advancedSearchField" type="text" class="form-control" aria-label="advancedSearchField" aria-describedby="advancedSearchField">
      <select id="choicesSelect" style="display: hide;" class="form-control"></select>
        
      <style>.noUi-connect {
        background: #0e0076;
      }</style>
      <div id="spacer" style="height:10px;"></div>
      <div id="date-input" class="input-group d-none">
        <span class="input-group-text">Begin:</span>
        <input type="number" aria-label="start-date" value="${min_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
        <span class="input-group-text">End:</span>
        <input type="number" aria-label="end-date" value="${max_year}" pattern="\d{4}"  maxlength="4" class="form-control"></input>
      </div>
      
      <label class="btn btn-sm  " for="addAND">or</label> 
                 
      <select id="searchSelect2" class="input-group form-select form-select-sm">
        
        <option value="">Please select...</option>
        <option value="deep-id">DEEP ID</option>
        <option value="brit-drama-number">BritDrama #</option>
        <option value="title" selected>Title</option>
        <option value="title-page-modern">All Title-Page Text (modern spelling)</option>
        <option value="title-page-old">All Title-Page Text (old spelling)</option>  
        <option value="author">Author (Modern Attribution)</option>
        <option value="title-page-author">Author (Title-Page Attribution)</option>
        <option value="authorial-status">Authorial Status (Title-Page Attribution)</option>
        <option value="company-first-performance">Company (First Production)</option>
        <option value="company_first-performance-brit-filter">Company of First Performance (BritDrama)</option>
        <option value="company">Company (Title-Page Attribution)</option>
        <option value="theater">Theater (Title-Page Attribution)</option>
        <option value="playtype">Play Type</option>
        <option value="genre">Genre (Annals)</option>
        <option value="genre-brit-filter">Genre (BritDrama)</option>
        <option value="genreplaybook" >Genre (Title-Page Attribution)</option>
        <option value="paratextual" >All Paratextual Material</option>
        <option value="illustration">Illustration</option>
        <option value="blackletter">Black Letter</option>
        <option value="latinontitle">Latin on Title Page</option>
        <option value="stationer">Stationer</option>
        <option value="printer" >&nbsp;&nbsp;&nbsp;&nbsp;Printer</option>
        <option value="publisher" >&nbsp;&nbsp;&nbsp;&nbsp;Publisher</option>
        <option value="bookseller" >&nbsp;&nbsp;&nbsp;&nbsp;Bookseller</option>
        <option value="imprintlocation">Imprint Location</option>
        <option value="first-production">Date of First Production</option>
        <option value="date-first-performance-brit-filter">Date of First Performance (BritDrama)</option>
        <option value="first-edition">Date of First Edition</option>
        <option value="format">Format</option>
        <option value="book_edition">Book edition number</option>
        <option value="play_edition">Play edition number</option>
        <option value="greg_number">Greg Number</option>
        <option value="stc_or_wing">STC / Wing Number</option>
        <option value="year-published">Year Published</option>
        <option value="dedication">Dedication</option>
        <option value="toreader">To the Reader</option>
        <option value="argument">Argument</option>
        <option value="actor-list">Actor List</option>
        <option value="explicit">Explicit</option>
        <option value="errata">Errata</option>
        <option value="charachter-list">Character List</option>
        <option value="other-paratexts">Other Paratexts</option>
        <option value="commendatory-verses" >Commendatory Verses</option>

      </select>
      <input id="advancedSearchField" type="text" class="form-control" aria-label="advancedSearchField" aria-describedby="advancedSearchField">
      <select id="choicesSelect" style="display: hide;" class="form-control"></select>
        
      <style>.noUi-connect {
        background: #0e0076;
      }</style>
      <div id="spacer" style="height:10px;"></div>
      <div id="date-input" class="input-group d-none">
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
  newBlock.id = 'filterBlock-'+document.getElementById('filterBlocks').childElementCount
  // <div id="filterBlock" class="input-group-md">
  newBlock.dataset.type = "OR"
  
  
  // First input
  let searchSelect1 = newBlock.children[1].children[0]
  update_searchSelect(searchSelect1);
  searchSelect1.addEventListener('change', (event) => {
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
  update_searchSelect(searchSelect2, or=true);
  searchSelect2.addEventListener('change', (event) => {
    update_searchSelect(searchSelect2,or=true);
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
  const searchSelect = document.getElementById("searchSelect");
  update_searchSelect(searchSelect);
  searchSelect.addEventListener('change', (event) => {
    update_searchSelect(searchSelect);
    
  })
}
init_firstBlock();
 
const processQueries = queries => {
  
  const filters = [] 
  // https://stackoverflow.com/questions/67068405/dynamically-create-a-condition-in-javascript
  for (i in queries){
    let query = queries[i]
    if (query.blockType == 'AND') {
      if (query.searchField == 'title') {
        let title = item => (
            item.title.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.title_alternative_keywords.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':title,'type':query.blockType})
      }
      if (query.searchField == 'stationer') { 
        let stationer = item => (
            item.stationer_printer.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.stationer_publisher.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.stationer_bookseller.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':stationer,'type':query.blockType})
      }
      if (query.searchField == 'paratextual') {
        let paratextual = item => (
            item.paratext_dedication.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_commendatory_verses.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_to_the_reader.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_argument.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_actor_list.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_charachter_list.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_errata.toLowerCase().includes(query.searchValue.toLowerCase()) || 
            item.paratext_other_paratexts.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':paratextual,'type':query.blockType})
        
      }
      if (query.searchField == 'commendatory-verses') {
        let commendatoryVerses = item => (
            item.paratext_commendatory_verses.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':commendatoryVerses,'type':query.blockType})
      }
      if (query.searchField == 'title-page-modern') {
        let titlePageModern = item => (
            item.title_page_modern_spelling.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':titlePageModern,'type':query.blockType})
      }
      if (query.searchField == 'imprintlocation') {
        let imprintLocation = item => (
            item.title_page_imprint.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':imprintLocation,'type':query.blockType})
      }
      if (query.searchField == 'title-page-old') {
        let titlePageOld = item => (
            item.title_page_title.toLowerCase().includes(query.searchValue.toLowerCase()) ||
            item.title_page_author.toLowerCase().includes(query.searchValue.toLowerCase()) ||
            item.title_page_performance.toLowerCase().includes(query.searchValue.toLowerCase()) ||
            item.title_page_latin_motto.toLowerCase().includes(query.searchValue.toLowerCase()) ||
            item.title_page_imprint.toLowerCase().includes(query.searchValue.toLowerCase())
            )
        filters.push({'filter':titlePageOld,'type':query.blockType})
      }
      if (query.searchField == 'title-page-author') {
        let titlePageAuthor = item => (
          item.title_page_author.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':titlePageAuthor,'type':query.blockType})
      }
      if (query.searchField == 'actor-list') {
        let actorList = item => (
          item.paratext_actor_list.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':actorList,'type':query.blockType})
      }
      if (query.searchField == 'explicit') {
        let explicit = item => (
          item.title_page_explicit.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':explicit,'type':query.blockType})
      }
      if (query.searchField == 'toreader') {
        let toreader = item => (
          item.paratext_to_the_reader.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':toreader,'type':query.blockType})
      }
      if (query.searchField == 'argument') {
        let argument = item => (
          item.paratext_argument.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':argument,'type':query.blockType})
      }
      if (query.searchField == 'dedication') {
        let dedication = item => (
          item.paratext_dedication.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':dedication,'type':query.blockType})
      }
      if (query.searchField == 'charachter-list') {
        let charachterList = item => (
          item.paratext_charachter_list.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':charachterList,'type':query.blockType})
      }
      if (query.searchField == 'errata') {
        let errata = item => (
          item.paratext_errata.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':errata,'type':query.blockType})
      }
      if (query.searchField == 'other-paratexts') {
        let otherParatexts = item => (
          item.paratext_other_paratexts.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':otherParatexts,'type':query.blockType})
      }
      if (query.searchField == 'illustration') {
        let illustration = item => (
          item.title_page_illustration.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':illustration,'type':query.blockType})
      }
      if (query.searchField == 'latinontitle') {
        let latinontitle = item => (
          item.title_page_latin_motto.toLowerCase().includes(query.searchValue.toLowerCase())
        )
        filters.push({'filter':latinontitle,'type':query.blockType})
      }
      if (query.searchField == 'deep-id') {
        let deepID = item => (
          item.deep_id.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':deepID,'type':query.blockType})
      }
      if (query.searchField == 'greg_number') {
        let gregNumber = item => (
          item.greg_full.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':gregNumber,'type':query.blockType})
      }
      if (query.searchField == 'book_edition') {
        let bookEdition = item => (
          item.book_edition.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':bookEdition,'type':query.blockType})
      }
      if (query.searchField == 'play_edition') {
        let playEdition = item => (
          item.play_edition.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':playEdition,'type':query.blockType})
      }
      if (query.searchField == 'stc_or_wing') {
        let stcWing = item => (
          item.stc.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':stcWing,'type':query.blockType})
      }
      if (query.searchField == 'author') {
        
        let author = item => (
          item.author.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':author,'type':query.blockType})
      }
      if (query.searchField == 'authorial-status') {
        let authorialStatus = item => (
          item.title_page_author.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':authorialStatus,'type':query.blockType})
      }
      if (query.searchField == 'blackletter') {
        let blackletter = item => (
          item.blackletter.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':blackletter,'type':query.blockType})
      }
      if (query.searchField == 'genre') {
        let genre = item => (
          item.genre.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':genre,'type':query.blockType})
      }
      if (query.searchField == 'format') {
        let format = item => (
          item.format.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':format,'type':query.blockType})
      }
      if (query.searchField == 'playtype') {
        let playtype = item => (
          item.play_type.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':playtype,'type':query.blockType})
      }
      if (query.searchField == 'company') {
        let company = item => (
          item.company_attribution.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':company,'type':query.blockType})
      }
      if (query.searchField == 'company-first-performance') {
        let companyFirstPerformance = item => (
          item.company_first_performance.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':companyFirstPerformance,'type':query.blockType})
      }
      if (query.searchField == 'dedication') {
        let dedication = item => (
          item.paratext_dedication.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':dedication,'type':query.blockType})
      }
      if (query.searchField == 'printer') {
        let printer = item => (
          item.stationer_printer.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':printer,'type':query.blockType})
      }
      if (query.searchField == 'publisher') {
        let publisher = item => (
          item.stationer_publisher.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':publisher,'type':query.blockType})
      }
      if (query.searchField == 'bookseller') {
        let bookseller = item => (
          item.stationer_bookseller.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':bookseller,'type':query.blockType})
      }
      if (query.searchField == 'brit-drama-number') {
        let britDrama = item => (
          item.brit_drama_number.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':britDrama,'type':query.blockType})
      }
      if (query.searchField == 'authorial-status') {
        let authorialStatus = item => (
          item.author_status.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':authorialStatus,'type':query.blockType})
      }
      if (query.searchField == 'theater') {
        let theater = item => (
          item.theater.toLowerCase().includes(query.searchValue.toLowerCase()) ||
          item.theater_type.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':theater,'type':query.blockType})
      }
      if (query.searchField == 'year-published') {
        let [ start, end ] = query.searchValue.split('-')
        let yearPublished = item => (
          item.year_int >= start && item.year_int <= end 
          )
        filters.push({'filter':yearPublished,'type':query.blockType})
      }
      if (query.searchField == 'first-production') {
        let [ start, end ] = query.searchValue.split('-')
        let firstProduction = item => (
          item.composition_date >= start && item.composition_date <= end 
          )
        filters.push({'filter':firstProduction,'type':query.blockType})
      }
      if (query.searchField == 'first-edition') {
        let [ start, end ] = query.searchValue.split('-')
        let firstEdition = item => (
          item.date_first_publication >= start && item.date_first_publication <= end 
          )
        filters.push({'filter':firstEdition,'type':query.blockType})
      }
    }
//OR!
    if (query.blockType == 'OR') { 
      // build two separate filters, then join them 
      let fields = query.searchField.split('||')
      let values = query.searchValue.split('||')
      let ORquery = []
      for (let i = 0; i < fields.length; i++) {
        if (fields[i] == 'title' && !values[i] =='') {
          let title = item => (
              item.title.toLowerCase().includes(values[i].toLowerCase()) || 
              item.title_alternative_keywords.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(title)
        }
        if (fields[i] == 'stationer' && values[i]) { 
          let stationer = item => (
              item.stationer_printer.toLowerCase().includes(values[i].toLowerCase()) || 
              item.stationer_publisher.toLowerCase().includes(values[i].toLowerCase()) || 
              item.stationer_bookseller.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(stationer)
        }
        if (fields[i] == 'paratextual' && values[i]) {
          let paratextual = item => (
              item.paratext_dedication.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_commendatory_verses.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_to_the_reader.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_argument.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_actor_list.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_charachter_list.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_errata.toLowerCase().includes(values[i].toLowerCase()) || 
              item.paratext_other_paratexts.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(paratextual)
        }
        if (fields[i] == 'commendatory-verses' && values[i]) {
          let commendatoryVerses = item => (
              item.paratext_commendatory_verses.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(commendatoryVerses)
        }
        if (fields[i] == 'title-page-modern' && values[i]) {
          let titlePageModern = item => (
              item.title_page_modern_spelling.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(titlePageModern)
        }
        if (fields[i] == 'imprintlocation' && values[i]) {
          let imprintLocation = item => (
              item.title_page_imprint.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(imprintLocation)
        }
        if (fields[i] == 'title-page-old' && values[i]) {
          let titlePageOld = item => (
              item.title_page_title.toLowerCase().includes(values[i].toLowerCase()) ||
              item.title_page_author.toLowerCase().includes(values[i].toLowerCase()) ||
              item.title_page_performance.toLowerCase().includes(values[i].toLowerCase()) ||
              item.title_page_latin_motto.toLowerCase().includes(values[i].toLowerCase()) ||
              item.title_page_imprint.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(titlePageOld)
        }
        if (fields[i] == 'title-page-author' && values[i]) {
          let titlePageAuthor = item => (
              item.title_page_author.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(titlePageAuthor)
        }
        if (fields[i] == 'actor-list' && values[i]) {
          let actorList = item => (
              item.paratext_actor_list.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(actorList)
        }
        if (fields[i] == 'explicit' && values[i]) {
          let explicit = item => (
              item.title_page_explicit.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(explicit)
        }
        if (fields[i] == 'toreader' && values[i]) {
          let toreader = item => (
              item.paratext_to_the_reader.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(toreader)
        }
        if (fields[i] == 'brit-drama-number' && values[i]) {
          let britDrama = item => (
              item.brit_drama_number.toLowerCase().includes(values[i].toLowerCase())
              )
              ORquery.push(britDrama)
        }
        if (fields[i] == 'argument' && values[i]) {
          let argument = item => (
             item.paratext_argument.toLowerCase().includes(values[i].toLowerCase())
            )
            ORquery.push(argument)
        }
        if (fields[i] == 'dedication' && values[i]) {
          let dedication = item => (
            item.paratext_dedication.toLowerCase().includes(values[i].toLowerCase())
            )
            ORquery.push(dedication)
        }
        if (fields[i] == 'charachter-list' && values[i]) {
          let charachterList = item => (
            item.paratext_charachter_list.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(charachterList)
        }
        if (fields[i] == 'errata' && values[i]) {
          let errata = item => (
            item.paratext_errata.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(errata)
        }
        if (fields[i] == 'other-paratexts' && values[i]) {
          let otherParatexts = item => (
            item.paratext_other_paratexts.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(otherParatexts)
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
          let deepID = item => (
            item.deep_id.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(deepID)
        }
        if (fields[i] == 'greg_number' && values[i]) {
          let gregNumber = item => (
            item.greg_full.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(gregNumber)
        }
        if (fields[i] == 'book_edition' && values[i]) {
          let bookEdition = item => (
            item.book_edition.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(bookEdition)
        }
        if (fields[i] == 'play_edition' && values[i]) {
          let playEdition = item => (
            item.play_edition.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(playEdition)
        }
        if (fields[i] == 'stc_or_wing' && values[i]) {
          let stcWing = item => (
            item.stc.toLowerCase().includes(values[i].toLowerCase())
          )
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
            item.author_status.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(authorialStatus)
        }
        if (fields[i] == 'blackletter' && values[i]) {
          let blackletter = item => (
            item.blackletter.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(blackletter)
        }
        if (fields[i] == 'genre' && values[i]) {
          let genre = item => (
            item.genre.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(genre)
        }
        if (fields[i] == 'format' && values[i]) {
          let format = item => (
            item.genre.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(format)
        }
        if (fields[i] == 'playtype' && values[i]) {
          let playtype = item => (
            item.play_type.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(playtype)
        }
        if (query.searchField == 'company') {
        let company = item => (
          item.company_attribution.toLowerCase().includes(query.searchValue.toLowerCase())
          )
        filters.push({'filter':company,'type':query.blockType})
        }
        if (fields[i] == 'company-first-performance' && values[i]) {
          let companyFirstPerformance = item => (
            item.company_first_performance.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(companyFirstPerformance)
        }
        if (fields[i] == 'dedication' && values[i]) {
          let dedication = item => (
            item.paratext_dedication.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(dedication)
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
        if (fields[i] == 'authorial-status' && values[i]) {
          let authorialStatus = item => (
            item.author_status.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(authorialStatus)
        }
        if (fields[i] == 'theater' && values[i]) {
          let theater = item => (
            item.theater.toLowerCase().includes(values[i].toLowerCase()) ||
            item.theater_type.toLowerCase().includes(values[i].toLowerCase())
          )
          ORquery.push(theater)
        }
        if (fields[i] == 'year-published' && values[i]) {
          let [ start, end ] = values[i].split('-')
          let yearPublished = item => (
            item.year_int >= start && item.year_int <= end 
          )
          ORquery.push(yearPublished)
        }
        if (fields[i] == 'first-production' && values[i]) {
          let [ start, end ] = values[i].split('-')
          let firstProduction = item => (
            item.composition_date >= start && item.composition_date <= end 
          )
          ORquery.push(firstProduction)
        }
        if (fields[i] == 'first-edition' && values[i]) {
          let [ start, end ] = values[i].split('-')
          let firstEdition = item => (
            item.date_first_publication >= start && item.date_first_publication <= end 
          )
          ORquery.push(firstEdition)
        }
      }
      filters.push({'filter':ORquery,'type':'OR'})
    }
    let singlePlay = document.getElementById('singlePlay') 
    if (!singlePlay.checked) {
      let singlePlayFilter = item => item.record_type != 'Single-Play Playbook'
      filters.push({'filter':singlePlayFilter,'type':'AND'})
    }
    let Collections = document.getElementById('Collections')
    if (!Collections.checked) {
      let collectionsFilter = item => item.record_type != 'Collection'
      filters.push({'filter':collectionsFilter,'type':'AND'})
    }
    let PlaysinCollections = document.getElementById('PlaysinCollections')
    if (!PlaysinCollections.checked) {
      let playsinCollections = item => item.record_type != 'Play in Collection'
      filters.push({'filter':playsinCollections,'type':'AND'})
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
  const results = filters.reduce(
      (d, f) => {
        if (f.type == "AND") { 
          return d.filter(f.filter) 
        } 
        if (f.type == "OR") { 
          if (f.filter.length == 1) { 
            return d.filter(f.filter[0])
          }
          if (f.filter.length == 2){
            return d.filter(f.filter[0]).concat(d.filter(f.filter[1]))
          }
        } 
      }, 
      item_array
  )
  console.log('results',results)
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
    let groups = groupBy(results, 'greg');
    
    for (i in groups) {
      if (groups[i].length == 1) {
        grouped_results.push(groups[i][0])
      } else {
        // sort the group by deep_id, return only lowest deep id
        let d = groups[i].sort((a,b) => a.deep_id - b.deep_id);
        grouped_results.push(d[0])
      }
    }
  } else if (filter == 'edition') {
    let groups = groupBy(results, 'greg_middle');
    for (i in groups) {
      if (groups[i].length == 1) {
        grouped_results.push(groups[i][0])
      } else {
        // sort the group by deep_id, return only lowest deep id
        let d = groups[i].sort((a,b) => a.deep_id - b.deep_id);
        grouped_results.push(d[0])
      }
      
      
    };
  } else if (filter == 'record') {
    grouped_results = results
  }
  resultCount = document.getElementById("resultCount")
  resultCount.innerText = grouped_results.length
  table.add(grouped_results);
  table.update();
}




          
// Section for record type filtering
const singlePlay = document.getElementById('singlePlay') 
singlePlay.addEventListener('change', (event) => {
  console.log('click!')
  search();
});

const Collections = document.getElementById('Collections')
Collections.addEventListener('change', (event) => {
  search();
});

const PlaysinCollections = document.getElementById('PlaysinCollections')
PlaysinCollections.addEventListener('change', (event) => {
  search();
});

const advancedSearchField = document.getElementById('advancedSearchField')
advancedSearchField.addEventListener('keyup', (event) => {
  search();
});


      
function expand(e, id) {
  changeButtonCollapse();
  let data = item_data[id];
  e.outerHTML = `
  <tr id="${data.id}" onclick="collapse(this, ${data.id});"><td class="deep_id">${data.deep_id}</td><td class="year">${data.year}</td><td class="authors_display">${data.authors_display}</td><td class="title">${data.title}</td><td>Collapse</td>
    <tr id="${data.id}-exp">
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
                ${!data.deep_id ? '' : '<span class="expand">DEEP #: </span><span id="deep_id"><a target="_blank" href="'+ data.deep_id +'.html">' + data.deep_id + '</a></span><br>'}
                ${!data.brit_drama_number ? '' : '<span class="expand">BritDrama #: </span><span id="deep_id">' + data.brit_drama_number + '</span><br>'}
                ${!data.greg_full ? '' : '<span class="expand">Greg #: </span><span id="greg_full">' + data.greg_full + '</span><br>'}
                ${!data.stc ? '' : '<span class="expand">STC/WING: </span><span id="stc"> ' + data.stc + '</span><br>'}
                ${!data.book_edition ? '' : '<span class="expand">Book Edition: </span><span id="book_edition"> ' + data.book_edition + '</span><br>'}
                ${!data.play_edition ? '' : '<span class="expand">Play Edition: </span><span id="play_edition"> ' + data.play_edition + '</span><br>'}
                ${!data.format ? '' : '<span class="expand">Format: </span><span id="format"> ' + data.format + '</span><br>'}
                ${!data.leaves ? '' : '<span class="expand">Leaves: </span><span id="leaves"> ' + data.leaves + '</span><br>'}
              </p>
            </div>    
            
            <div class="col-7">
              <p>
                ${!data.record_type ? '' : '<span class="expand">Record Type: </span><span id="record_type">' + data.record_type + '</span><br>'}
                ${!data.play_type ? '' : '<span class="expand">Play Type: </span><span id="play_type">' + data.play_type + '</span><br>'}
                ${!data.genre ? '' : '<span class="expand">Genre (Annals): </span><span id="genre">' + data.genre + '</span><br>'}
                ${!data.genre_brit_display ? '' : '<span class="expand">Genre (BritDrama): </span><span id="genre">' + data.genre_brit_display + '</span><br>'}
                ${!data.date_first_publication ? '' : '<br><span class="expand">Date of First Publication: </span><span id="date_first_publication">' + data.date_first_publication + '</span><br>'}
                ${!data.date_first_performance ? '' : '<span class="expand">Date of First Performance: </span><span id="date_first_performance">' + data.date_first_performance + '</span><br>'}
                ${!data.date_first_performance_brit_display ? '' : '<span class="expand">Date of First Performance (BritDrama): </span><span id="date_first_performance">' + data.date_first_performance_brit_display + '</span><br>'}
                ${!data.company_first_performance ? '' : '<span class="expand">Company of First Performance: </span><span id="company_first_performance">' + data.company_first_performance + '</span><br>'}
                ${!data.company_first_performance_brit_display ? '' : '<span class="expand">Company of First Performance (BritDrama): </span><span id="company_first_performance">' + data.company_first_performance_brit_display + '</span><br>'}
                ${!data.company_attribution ? '' : '<span class="expand">Company Attribution: </span><span id="company_attribution">' + data.company_attribution + '</span><br>'}
              </p>
            </div>

            <div class="col-12">
              <p>
                ${typeof data.total_editions === 'undefined' ? '' : '<br><span class="expand">Total Editions:</span><span id="total_editions"> ' + data.total_editions + '</span><br>'}
                ${data.variants === '' ? '' : '<br><span class="expand">Variants:</span><span id="variants"> ' + data.variants + ' ' + data.variant_link + '<br>'}
                ${data.in_collection === '' ? '' : '<br><span class="expand">In Collection:</span><span id="in_collection"> ' + data.in_collection + '</span><br>'}
                ${data.collection_contains === '' ? '' : '<br><span class="expand">Collection Contains:</span><span id="collection_contains"> ' + data.collection_contains + '</span><br>'}
                ${!data.independent_playbook ? '' : '<br><span class="expand">Also appears as a bibliographically independent playbook in </span><span id="independent_playbook"><a target="_blank" href="' + data.independent_playbook_link_id + '.html">' + data.independent_playbook + '</a></span><br>'}
                ${!data.also_in_collection ? '' : '<br><span class="expand">Also appears in collection: </span><span id="also_in_collection">' + data.also_in_collection_link + '</span><br>'}
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
                ${!data.title_page_title ? '' : '<span class="expand">Title: </span><span id="title_page_title">' + data.title_page_title + '</span><br>'}
                ${!data.title_page_author ? '' : '<span class="expand">Author: </span><span id="title_page_author">' + data.title_page_author + '</span><br>'}
                ${!data.title_page_performance ? '' : '<span class="expand">Performance: </span><span id="title_page_performance">' + data.title_page_performance + '</span><br>'}
                ${!data.title_page_imprint ? '' : '<span class="expand">Imprint: </span><span id="title_page_imprint">' + data.title_page_imprint + '</span><br>'}
                ${!data.title_page_colophon ? '' : '<span class="expand">Colophon: </span><span id="title_page_colophon">' + data.title_page_colophon + '</span><br>'}
                ${!data.title_page_illustration ? '' : '<span class="expand">Illustration: </span><span id="title_page_illustration">' + data.title_page_illustration + '</span><br>'}
                ${!data.title_page_latin_motto ? '' : '<span class="expand">Latin Motto: </span><span id="title_page_latin_motto">' + data.title_page_latin_motto + '</span><br>'}
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
                ${!data.paratext_dedication && !data.paratext_commendatory_verses && !data.paratext_to_the_reader && !data.paratext_errata && !data.paratext_argument && !data.paratext_charachter_list && !data.paratext_actor_list && !data.paratext_other_paratexts ? 'None' : ""}
                ${!data.paratext_dedication ? '' : '<span class="expand">Dedication: </span><span id="paratext_dedication">' + data.paratext_dedication + '</span><br>'}
                ${!data.paratext_commendatory_verses ? '' : '<span class="expand">Commendatory Verses: </span><span id="paratext_commendatory_verses">' + data.paratext_commendatory_verses + '</span><br>'}
                ${!data.paratext_to_the_reader ? '' : '<span class="expand">To the Reader: </span><span id="paratext_to_the_reader">' + data.paratext_to_the_reader + '</span><br>'}
                ${!data.paratext_errata ? '' : '<span class="expand">Errata: </span><span id="paratext_errata">' + data.paratext_errata + '</span><br>'}
                ${!data.paratext_argument ? '' : '<span class="expand">Argument: </span><span id="paratext_argument">' + data.paratext_argument + '</span><br>'}
                ${!data.paratext_charachter_list ? '' : '<span class="expand">Charachter List: </span><span id="paratext_charachter_list">' + data.paratext_charachter_list + '</span><br>'}
                ${!data.paratext_actor_list ? '' : '<span class="expand">Actor List: </span><span id="paratext_actor_list">' + data.paratext_actor_list + '</span><br>'}
                ${!data.paratext_other_paratexts ? '' : '<span class="expand">Other: </span><span id="paratext_other_paratexts">' + data.paratext_other_paratexts + '</span><br>'}
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
                ${!data.stationer_printer && !data.stationer_publisher && !data.stationer_bookseller && data.stationer_entries_in_register === "None" && !data.stationer_additional_notes ? 'None' : '' }
                ${!data.stationer_printer ? '' : '<span class="expand">Printer: </span><span id="stationer_printer">' + data.stationer_printer + '</span><br>'}
                ${!data.stationer_publisher ? '' : '<span class="expand">Publisher: </span><span id="stationer_publisher">' + data.stationer_publisher + '</span><br>'}
                ${!data.stationer_bookseller ? '' : '<span class="expand">Bookseller: </span><span id="stationer_bookseller">' + data.stationer_bookseller + '</span><br>'}
                ${data.stationer_entries_in_register === "None" ? "" : "<span class='expand'>Entries in Stationers' Register: </span><span id='stationer_entries_in_register'>" + data.stationer_entries_in_register + '</span><br>'}
                ${!data.stationer_additional_notes ? '' : '<span class="expand">Additional Notes: </span><span id="stationer_additional_notes">' + data.stationer_additional_notes + '</span><br>'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </td>
    
  </tr>`;
}


function collapse(e, id) {
  
    let data = item_data[id];
    if (data) {
      e.outerHTML = `
      <tr id="${data.id}" onclick="expand(this, ${data.id});"><td class="deep_id">${data.deep_id}</td><td class="year">${data.year}</td><td class="authors_display">${data.authors_display}</td><td class="title">${data.title}</td><td>Expand</td>`
      let expandCard = document.getElementById(id+'-exp');
      if (expandCard) {
        expandCard.remove();
      }
    }
  }

function changeButtonCollapse() {
  let changeButton = document.getElementById('expandAllButton')
  changeButton.textContent = 'Collapse All';
  changeButton.setAttribute( "onClick", "collapseAll(this)" );
}
  

function expandAll(e) { 
  e.textContent = 'Collapse All';
  e.setAttribute( "onClick", "collapseAll(this)" );
  let items = document.querySelectorAll('tr');
  items.forEach(function(item) {
    expand(item, item.id);
  });
}

function collapseAll(e){
  e.textContent = 'Expand All';
  e.setAttribute( "onClick", "expandAll(this)" );
  let items = document.querySelectorAll('tr');
  items.forEach(function(item) {
    if (!item.id.includes("-exp")) {
      collapse(item, item.id);
    }
  });

};

function radioHelper(){
  if (document.getElementById('titleRadio').checked){
    return 'title';
  }
  else if (document.getElementById('editionRadio').checked){
    return 'edition';
  }
  else if (document.getElementById('recordRadio').checked){
    return 'record';
  }
}

// listen for radio filter changes

document.querySelectorAll('input[type=radio]').forEach(item => {
  item.addEventListener('change', event => {
    search();
  })
})


  const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const deep_id = urlParams.get('deep_id') // returns null if not in url
    if (deep_id) {
      // NOTE requires user to allow pop-up
      window.open(`${deep_id}.html`);
    }
   
