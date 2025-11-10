import { fetchSources } from '@apis'

export const useFilterStore = defineStore('filter', {
  state: () => ({
    // init filter
    sources: [],

    // filter params
    source: null,
    tri: 'date',
    window: 48,
    searchQuery: '',
    

  }),
  actions: {
    async initialize(storePosts) {
      const sources  = await fetchSources()
      console.log(sources)
      this.sources = sources

      this.dossier =  storePosts.dossier;
      this.tri = storePosts.tri;
      this.window =  storePosts.window;
      this.searchQuery =  storePosts.searchQuery;

    },
    updateFilter(fieldName, value) {
      if (Object.prototype.hasOwnProperty.call(this, fieldName)) {
        this[fieldName] = value;
      } else {
        console.warn(`Field "${fieldName}" does not exist in the store.`);
      }
    }
  },
  persist: true,
})

