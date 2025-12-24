<script lang="ts">
  import ArmySelector from './lib/ArmySelector.svelte'
  import './app.css'
</script>

<main>
  <ArmySelector />
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }

  :global(html) {
    background: #1e1e1e;
  }

  main {
    width: 100%;
  }
</style>
