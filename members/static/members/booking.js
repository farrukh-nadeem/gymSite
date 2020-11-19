document.addEventListener('DOMContentLoaded', function() {
	//console.log('I am at top')
	document.querySelector('#filters_view').style.display = 'block';
	document.querySelector('#all_services_view').style.display = 'block';
	document.getElementById('search_services').addEventListener('click', view_selected_services);
	// console.log(search);
	// if(search){
	// 	console.log('Iam clicked')
	// 	search.addEventListener('click', view_selected_services);
	// }
	let slider = document.getElementById("myRange");
	let output = document.getElementById("demo");
	output.innerHTML = slider.value;

	slider.oninput = function() {
	  output.innerHTML = this.value;
	}
});

function view_selected_services(){
	document.querySelector('#service_heading').style.display = 'block';
	document.querySelector('#all_services_view').style.display = 'none';
	document.querySelector('#selected_service_view').innerHTML = '';
	const type_id_var = document.querySelector('#service_type').value;
	if (type_id_var == 'all'){
		type_id = 0;
	}
	else{
		type_id = parseInt(type_id_var);
	}
	const service_loc = document.querySelector('#service_where').value;
	const days = document.querySelector('#days').value;
	const timing = document.querySelector('#timing').value;
	const exID_var = document.querySelector('#exercise').value;
	if (exID_var == 'all'){
		exID = 0;
	}
	else{
		exID = parseInt(exID_var);
	}
	//const min_price = document.querySelector('#minRange').value;
	//const max_price = document.querySelector('#myRange').value;
	//minCharges = parseInt(min_price);
	//maxCharges = parseInt(max_price);
	let maxCharges = document.getElementById("myRange").value;
	maxCharges = parseInt(maxCharges)
	 console.log(maxCharges)
	 console.log(type_id,service_loc,days,timing,exID,maxCharges)

	fetch(`selected_services/${type_id}/${service_loc}/${days}/${timing}/${exID}/${maxCharges}`)
	.then(response => response.json())
	.then(services => {
		//document.querySelector('#all_services_view').style.display = 'none';
		//console.log(services)
		for(i=0; i<services.length; i++){
			const service_display = document.createElement('div');//service_display is for service div
			service_display.setAttribute('class', 'inside');
			service_display.setAttribute('data-id', `${i}`);
			sessionType= 'Group';
			sessionPlace = 'On Site'
			if(services[i].is_Online == true){
				sessionPlace = 'Online'
			}
			if(services[i].is_oneToOne == true){
				sessionType = 'One To One'
			}
			service_display.innerHTML=`
			   <div class="card" style="width: 18rem; margin: 20px;">
			     <div class="card-body">
			       <h3 class="card-title">${services[i].exercise}</h3>
			       <h5 class="card-title">${services[i].type}</h5>
			       <h6 class="card-subtitle mb-2 text-muted">By ${services[i].serviceProvider}</h6>
			       <p class="card-text"> 
			       		<b>Mode: </b> ${sessionPlace} <br>
			       <b> Price: </b>${services[i].charges} </p>
			       <a href="confirm_booking/${services[i].id}" class="link">
			       		<button class="book_details">Get Access</button>
			       </a>
			     </div>
			   </div>`
			document.querySelector('#selected_service_view').append(service_display);
			document.querySelector('#selected_service_view').style.display = 'block';
		}
		
	});
}