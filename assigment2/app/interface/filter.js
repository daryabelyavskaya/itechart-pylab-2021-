function getFilterUrl(filter_url,document){
    
     if (document.querySelector("postcategory").value){
         if (filter_url.searchParams.has('category')){
             filter_url.searchParams.append('category',document.querySelector("postcategory"))
         }
         filter_url.searchParams.set('date_min',querySelector("date-min"))
     }
     if (document.querySelector("date-min").value){
         if (filter_url.searchParams.has('date_min')){
             filter_url.searchParams.append('date_min',querySelector("date-min"))
         }
         filter_url.searchParams.set('date_min',querySelector("date-min"))
     }
     if (document.querySelector("date-max").value){
         if (filter_url.searchParams.has('date_max')){
             filter_url.searchParams.append("date_max="+ document.querySelector("date-max").value)
         }
         filter_url.searchParams.set("date-max",document.querySelector("numberofvotes-min").value)
     }
     if (document.querySelector("numberofvotes-min").value){
         if (filter_url.searchParams.has('votes_min')){
             filter_url.searchParams.append("votes_min",document.querySelector("numberofvotes-min").value)
         }
         filter_url.searchParams.set("votes_min",document.querySelector("numberofvotes-min").value)
     }
     if(document.querySelector("numberofvotes-max").value){
         if (filter_url.searchParams.has('votes_max')){
             filter_url.searchParams.append("votes_max",document.querySelector("numberofvotes-max").value)
         }
         filter_url.searchParams.set("votes_max",document.querySelector("numberofvotes-max").value)
     }
     return filter_url
}