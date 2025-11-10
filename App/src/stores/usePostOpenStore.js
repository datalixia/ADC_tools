
export const usePostOpenStore = defineStore('postOpen', {
  state: () => ({
    post:null,
    
  }),
  actions: {
    async update(post) {
      this.post = post
    },
    reset(){
      this.post = null
    }
  }
})

