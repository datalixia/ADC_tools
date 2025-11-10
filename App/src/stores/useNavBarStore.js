const { width: windowWidth } = useWindowSize()
export const useNavBarStore = defineStore('navbar', {
  state: () => ({
    // init filter
    isOpen:true,

  }),
  actions: {
    open(){
      this.isOpen = true
      windowWidth.value = windowWidth.value - 10e-12
    },
    close(){
      this.isOpen = false
      windowWidth.value = windowWidth.value - 10e-12
    }
  },

})

