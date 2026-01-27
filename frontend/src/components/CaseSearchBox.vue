<template>
  <div class="container-fluid d-flex justify-content-center mb-3">
    <div class="card shadow-sm p-3 w-100" style="max-width: 600px;">
      <input
        v-model="searchQuery"
        @input="onInput"
        type="text"
        class="form-control"
        placeholder="Filter cases (fuzzy matches as you type)..."
        aria-label="Filter cases"
      />
    </div>
  </div>
</template>

<script>
// Debounce utility
function debounce(fn, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), delay);
  };
}

export default {
  name: 'CaseSearchBox',
  emits: ['search'],
  data() {
    return {
      searchQuery: '',
      debouncedEmit: null
    };
  },
  methods: {
    onInput() {
      if (!this.debouncedEmit) {
        this.debouncedEmit = debounce((q) => {
          this.$emit('search', q);
        }, 300);
      }
      this.debouncedEmit(this.searchQuery);
    }
  }
};
</script>
