import { fetchPosts } from '@apis';

export const usePostsStore = defineStore('posts', {
  state: () => ({
    // filter
    current_title : null,
    source: null,
    tri: 'date',
    window: 48,
    searchQuery: '',
    

    // posts
    sources_images : [],
    loading:false,
    total:0,
    total_unread:0,
    next_page:0,
    size:40,
    posts: [],
    viewType : 'list',
    endLoad : false,
  }),
  actions: {
    initialize(){
      this.sources_images = []
      this.total = 0;
      this.total_unread = 0;
      this.next_page = 0;
      this.posts = [];
      this.loading = false;
      this.endLoad = false;
      this.current_title = null;
    },
    toggleView() {
      let newValue = 'list';
      if (this.viewType == 'list') {
        newValue = 'cards'
        
      }
      else{
        if (this.viewType == 'cards')  {
          newValue = 'list'
        }
      }

      this.viewType = newValue
      
    },

    async loadPosts() {
      
      if (this.endLoad) return; // Prevent call when end of data

      if (this.loading) return; // Prevent multiple calls while loading
        
      this.loading = true;


      try{

        // send request
        const data = await fetchPosts(this.source.source_name);

        // if api function return null, its an error
        if(data == null){
          throw new Error('error loading data');
        }

        // if length of returned data less than size of page, its the end
        if(data.data.length < this.size){
          this.endLoad = true
        }

        // update store fields
        this.posts.push(...data.data) 
        this.total = data.total
        this.total_unread = data.total - data.total_read
        this.next_page = this.next_page + data.per_page

        
        

      }
      catch(error){
        console.error(error);
      }
      finally{
        this.loading = false;
      }


    },
    async refreshPosts() {
      
      this.initialize()
      if (this.loading) return; // Prevent multiple calls while loading
      
      this.loading = true;

      try{


        // send request
        this.posts = [] // empty posts
        const data = await fetchPosts(this.source.source_name);

        // if api function return null, its an error
        if(data == null){
          throw new Error('error loading data');
        }

        // if length of returned data less than size of page, its the end
        if(data.data.length < this.size){
          this.endLoad = true
        }


        // change store fields
        this.posts = data.data
        this.total = data.total
        this.total_unread = data.total - data.total_read
        this.next_page = this.size

        

      }
      catch(error){
        // error when fetching data, make fields to init values
        this.initialize()
        console.error(error);
      }
      finally{
        this.loading = false;
      }


    },
    async refreshFilter(filter){
      this.source =  filter.source;
      this.tri = filter.tri;
      this.window =  filter.window;
      this.searchQuery =  filter.searchQuery;
      await this.refreshPosts()
    }

  },
  persist: true,
})

