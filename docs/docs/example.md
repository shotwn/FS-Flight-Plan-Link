<script src='/js/main.js' type='text/javascript'></script>

<style>
  
</style>
<div id='example'>
  <div id='example_button'>
  </div>
</div>

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

  let planClient = new fsfpl.Plan(plan, planOptions)
  // planClient.send()
</script>