<script src='../../js/main.js' type='text/javascript'></script>

# JavaScript Client Examples
## Loading Flight Plan Using JavaScript
#### Used Code

```HTML
<div id='example'>
  <div id='example_button'>
  </div>
</div>
```

```
let plan = {
'callsign': 'THYTST',
'departure': 'LTBA',
'destination': 'LTFM',
'route': 'LTBA LTFM'
}

let planOptions = {
	'buttons': [
		{
			to: 'example_button',
			text: 'Load Plan'
		}
	]
}

let planClient = new fsl.Plan(plan, planOptions)
```

#### Result

<div id='example'>
  <div id='example_button'>
  </div>
</div>

Button on this div is automatically generated with given options.

Clicking it will load the flight in the example code.

<script>
  let plan = {
    'callsign': 'THYTST',
    'departure': 'LTBA',
    'destination': 'LTFM',
    'route': 'LTBA LTFM'
  }

  let planOptions = {
    'buttons': [
      {
        to: 'example_button',
        text: 'Load Plan'
      }
    ]
  }

  let planClient = new fsl.Plan(plan, planOptions)
  // planClient.send()
</script>



## Pulling Data from Existing DOM Structure
### Turkish Virtual Departures Page

Using FSLink.collector we can pull data from DOM.

#### Used Code
```
const link = new fsl.FSLink()

function collectTv() {
	return new Promise((resolve, reject) => {
		/*
		* This is the important part. Rest is async mumbo jumbo
		*/
		link.collect({
			'route': {
				selector: '#route1',
				attribute: 'innerHTML'
			},
			'flight_code': {
				selector: '#flcode',
				attribute: 'innerHTML'
			},
			'departure': {
				selector: '#departure',
				attribute: 'innerHTML'
			},
			'destination': {
				selector: '#destination',
				attribute: 'innerHTML'
			},
			'alternate': {
				selector: '#alternate',
				attribute: 'innerHTML'
			},
			'callsign': {
				selector: '#callsign',
				attribute: 'innerHTML'
			},
			'block_time': {
				selector: '#time',
				attribute: 'innerHTML'
			},
			'aircraft': {
				selector: 'input[name="aircraft"]:checked',
				attribute: 'value'
			},
			'cruise_altitude': {
				selector: 'input[name="cruise-altitude"]:checked',
				attribute: 'value'
			}
		}).then(result => {
			document.getElementById('test-1-result').innerHTML = JSON.stringify(result, null, 2)
			console.log(result)
			resolve(result)
			/*
			* We would normally call 'send' here with result.
			* link.send(result)
			*
			* I am returning a promise instead for example purposes.
			*/
		})
		/*
		* End of async mumbo jumbo
		*/
	})
}

function sendTv(caller) {
	let options = {
		caller: caller
	}
	collectTv().then(result => {
		link.send(result, options)
	})
}
```

#### Example DOM
Following HTML example is a copy of Turkish Virtual's Departure Page. 

<table class="grid" align="center" 

<center><b><label id="tanitim" style="color:Black; font-size:large" visible=true><center>Turkish Virtual Dispatch Service</center></label></b></center>
</table>



<table class="grid">
<tr class="foot">
<td colspan="3" class="alnc bdrr clrr fntb" id="caption">
LTFM - ISTANBUL NEW AIRPORT / UKDE - MOKRAYA
</td>
</tr>
</table>

<table class="grid" >
<tr class="alnc clrr fntb" id="mettaf"><td>METAR and TAF Information</td></tr>
</table>


<table class="grid">
<tr class="capt bdrs"><td colspan="2"><center>Departure : <a id='departure' href="https://www.turkishvirtual.com/airports.asp?code=LTFM">LTFM</a> - ISTANBUL NEW AIRPORT (Click to see airport details)</center></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">METAR</td><td><div id="metar1">LTFM 142050Z 24010KT 9999 SCT035 BKN100 17/05 Q1012 NOSIG</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">TAF</td><td><div id="taf1">No TAF available for LTFM.</div></td></tr>
<tr class="foot"><td class="clrg" colspan="2"><center><b>Please check PILOT CENTRE for <a class="link" href="https://www.turkishvirtual.com/charts.asp">Charts</a> and <a class="link" href="https://www.turkishvirtual.com/scenerys.asp">Sceneries</a><br/></b></center></td></tr>
</table>

<table class="grid">
<tr class="capt bdrs"><td colspan="2"><center>Destination : <a id='destination' href="https://www.turkishvirtual.com/airports.asp?code=UKDE">UKDE</a> - MOKRAYA (Click to see airport details)</center></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg w64">METAR</td><td><div id="metar2">UKDE 141500Z 16006MPS 120V210 CAVOK 17/M00 Q1006 R20L/090070 NOSIG</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">TAF</td><td><div id="taf2">2019/12/20 16:09
TAF 
      AMD TAF 
      AMD UKDE 201606Z 2016/2124 09003MPS 0100 FZFG VV001 TXM01/2016Z TNM03/2124Z 
      TEMPO 2018/2021 1000 BR OVC003
</div></td></tr>
<tr class="foot"><td class="clrg" colspan="2"><center><b>Please check PILOT CENTRE for <a class="link" href="https://www.turkishvirtual.com/charts.asp">Charts</a> and <a class="link" href="http://www.turkishvirtual.com/scenerys.asp">Sceneries</a><br/></b></center></td></tr>
</table>

<table class="grid">
<tr class="capt bdrs"><td colspan="2"><center>Alternate : <a id="alternate" href="https://www.turkishvirtual.com/airports.asp?code=UKOH">UKOH</a> - KHERSON INTL (Click to see airport details)</center></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">METAR</td><td><div id="metar3"></div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">TAF</td><td><div id="taf3">No TAF available for UKOH.</div></td></tr>
<tr class="foot"><td class="clrg" colspan="2"><center><b>Please check PILOT CENTRE for <a class="link" href="https://www.turkishvirtual.com/charts.asp">Charts</a> and <a class="link" href="https://www.turkishvirtual.com/scenerys.asp">Sceneries</a><br/></b></center></td></tr>
</table>

<br>

<table class="grid" >
<tr class="alnc clrr fntb" id="mettaf"><td>ROUTE INFORMATION</td></tr>
</table>

<table class="grid" >
<tr class="seq1"><td class="alnr fntb clrr bckg" width="80">Route 1 :</td><td><div id="route1">MAKOL N617 OSDOR L743 KOSAK Y179 RAPUL L140 KH N604 DITIX</div></td></tr>
<tr class="foot"><td class="clrg" colspan="2"><center><b></b></center></td></tr>
</table>
<table class="grid" style="table-layout:fixed; width:620px">
<tr class="seq1"><td class="alnr fntb clrr bckg" width="80">Route 2 :</td><td style="word-break:break-all"><div id="route2">Not Available</div></td></tr>
<tr class="foot"><td class="clrg" colspan="2"><center><b></b></center></td></tr>
</table>

<div class='tab'><ul><li class='current'><a class="t"><span>Route of The Destination</span></a></li><li><span class='remark'>Turkish Virtual &bull; Information Services</span></li></ul></div>

<table class="grid">
<tr><td style="padding:0px;">
</td></tr>
</table>

<a>
<img src="https://turkishvirtual.com/img/Turkish_a.png" width="620" height="40"></img>
</a>
<div class='tab'><ul><li><span class='remark'> </span></li></ul></div>
</br>


<center><img src="https://turkishvirtual.com/img/schflight.jpg" width="620" height="161"></img></center><br>
<center>(This is a Scheduled Flight)</center>


<table class="grid" >
<tr class="alnc clrr fntb" id="othinf"><td>OTHER INFORMATION</td></tr>
</table>

<table class="grid">
<tr class="seq1"><td class="alnr fntb clrr bckg" width="80">Flight Code</td><td><div id="flcode">THY 1469</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">Callsign</td><td><div id="callsign">THY 2RD</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">Aircraft</td><td><div id="acs">
<div class="radio-toolbar">
	<input type="radio" id="aircraft_a319" name="aircraft" value="A319" checked>
	<label for="aircraft_a319">A319</label>
	<input type="radio" id="aircraft_a320" name="aircraft" value="A320">
	<label for="aircraft_a320">A320</label>
</div>

</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg" width="80">Flight Levels</td><td><div id="flvls">
<div class="radio-toolbar">
	<input type="radio" id="fl_1" name="cruise-altitude" value="33000" checked>
	<label for="fl_1">FL330</label>
	<input type="radio" id="fl_2" name="cruise-altitude" value="35000">
	<label for="fl_2">FL350</label>
</div>
</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">Distance</td><td><div id="distance">498 nm</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">Flight Time</td><td><div id="time">1:40</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">Flight Type</td><td><div id="fty">International Flight</div></td></tr>
<tr class="seq1"><td class="alnr fntb clrr bckg">Ticket Price</td><td><div id="fty">1400</div></td></tr>

<tr class="seq1"><td class="alnr fntb clrr bckg">Departure Time</td>
<td>
	<div id="fty">
		<datalist id="quick_times">
			<option value="14:40" title="Schedule Time">
			<option value="16:00">
			<option value="16:30">
		</datalist>
		<script>
		function formatTime(input) {
			if (input.value.length == 0) {
				return
			}
			if (!input.value.includes(':')) {
				input.value = input.value.slice(0,2) + ':' + input.value.slice(2, 4)
			}
			let spt = input.value.split(':')
			let h = spt[0].replace(/\D/g,'').slice(0,2).padStart(2, '0')
			let m = spt[1].replace(/\D/g,'').slice(0,2).padStart(2, '0')
			h = (h > 23) ? 23 : h
			h = (h < 0) ? 0 : h
			m = (m > 59) ? 59 : m
			m = (m < 0) ? 0 : m
			input.value = h + ':' + m
		}
		</script>
		<input style="max-width: 75px;" onblur="formatTime(this)" list='quick_times' type="text" id="departure_time" value="14:40" pattern="(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]" placeholder="HH:MM" maxlength=5>
			<button onclick="document.getElementById('departure_time').value = ''" title="Clear">X</button>
	</div>
</td></tr>

<tr class="foot"><td class="clrg" colspan="2"><center><b>Please check PILOT CENTRE for <a class="link" href="https://www.turkishvirtual.com/charts.asp">Charts</a> and <a class="link" href="https://www.turkishvirtual.com/scenerys.asp">Sceneries</a><br/></b></center></td></tr>
</table>


<div class="notes">
<b><i>Not for real aviation !</i></b>
</div>
		
</p>
</td>

<!--
ADDED
id field for: departure, destination, alternate
new field: departure_time
radio select for: aircraft, flight-level (cruise-altitude)
--->
<style>
	.radio-toolbar input[type="radio"] {
		display: none;
	}

	.radio-toolbar label {
		display: inline-block;
		background-color: #ddd;
		padding: 4px 11px;
		font-family: Arial;
		font-size: 16px;
		cursor: pointer;
	}

	.radio-toolbar input[type="radio"]:checked+label {
		background-color: #bbb;
	}
</style>

#### Result
<div style='border: 1px solid black; min-height: 250px; min-width:100%; white-space: pre;' id='test-1-result'></div>
<button class="btn btn-green" onClick='collectTv()'>Collect</button>
<button class="btn btn-green" onClick='sendTv(this)'>Send</button>

<script>
const link = new fsl.Utility()

function collectTv() {
	return new Promise((resolve, reject) => {
		/*
		* This is the important part. Rest is async mumbo jumbo
		*/
		link.collect({
			'route': {
				selector: '#route1',
				attribute: 'innerHTML'
			},
			'flight_code': {
				selector: '#flcode',
				attribute: 'innerHTML'
			},
			'departure': {
				selector: '#departure',
				attribute: 'innerHTML'
			},
			'destination': {
				selector: '#destination',
				attribute: 'innerHTML'
			},
			'alternate': {
				selector: '#alternate',
				attribute: 'innerHTML'
			},
			'callsign': {
				selector: '#callsign',
				attribute: 'innerHTML'
			},
			'block_time': {
				selector: '#time',
				attribute: 'innerHTML'
			},
			'aircraft': {
				selector: 'input[name="aircraft"]:checked',
				attribute: 'value'
			},
			'cruise_altitude': {
				selector: 'input[name="cruise-altitude"]:checked',
				attribute: 'value'
			},
			'departure_time': {
				selector: '#departure_time',
				attribute: 'value'
			}
		}).then(result => {
			document.getElementById('test-1-result').innerHTML = JSON.stringify(result, null, 2)
			console.log(result)
			resolve(result)
			/*
			* We would normally call 'send' here with result.
			* link.send(result)
			*
			* I am returning a promise instead for example purposes.
			*/
		})
		/*
		* End of async mumbo jumbo
		*/
	})
}

function sendTv(caller) {
	let options = {
		caller: caller
	}
	collectTv().then(result => {
		link.send(result, options)
	})
}
</script>