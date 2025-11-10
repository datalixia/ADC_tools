import { usePostsStore } from '@/stores/usePostsStore';
export function getIconPlateformes(platformeName) {
    const iconMap_for_platforms = {
        "TikTok": "tiktok.png",
        "YouTube": "youtube.png",
        "Youtube": "youtube.png",
        "LinkedIn": "linkedin.png",
        "Instagram": "instagram.png",
        "Twitter": "twitter.png",
        "Facebook": "facebook.png",
        "Google": "google.png",
        "Médias internationaux": "world.png",
        "Médias nationaux": "star.png"
      }
    const social = "/src/assets/images/plateformes/social"
    const iconSocial= new URL(social, import.meta.url).href;
    // Récupère le nom de fichier de l'icône correspondant à partir d'un objet JSON `iconMap_for_platforms`.
    const iconFileName = iconMap_for_platforms[platformeName];
    // Dynamically import the icon if it exists
    if (iconFileName) {
      const iconName = "/src/assets/images/plateformes/" + iconFileName
      const iconModule = new URL(iconName, import.meta.url).href;
      return iconModule || iconSocial;
    } else {
      return iconSocial; // Return default icon if no match
    }
}

export function timestampToDate(timestamp) {
    // Convert seconds to milliseconds if necessary
    try {
      if (timestamp.toString().length === 10) {
        timestamp *= 1000;
      }
  
      const date = new Date(timestamp);
      const day = String(date.getDate()).padStart(2, '0'); // Ensure 2 digits for day
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
      const year = date.getFullYear(); // Get full year
      const hours = String(date.getHours()).padStart(2, '0'); // Ensure 2 digits for hours
      const minutes = String(date.getMinutes()).padStart(2, '0'); // Ensure 2 digits for minutes
      return `${day}.${month}.${year} ${hours}:${minutes}`;
    } catch {
      console.log(timestamp)
      return ''
    }
  
  }

  export function stripHtmlTags(input) {
    const value = input.replace(/<[^>]*>/g, '')
    return value;
}



  export  function detectLanguage(text) {
    const arabicRegex = /[\u0600-\u06FF]/;
    const latinRegex = /[A-Za-z]/;
  
    if (arabicRegex.test(text)) return 'rtl';
    if (latinRegex.test(text)) return 'ltr';
    return 'ltr';
  }

  export function getIconSource(source_id){
    const store = usePostsStore()
    // Récupère le nom de fichier de l'icône correspondant à partir d'un objet JSON `iconMap_for_platforms`.
    const image = store.sources_images.find(item => item.id == source_id)
    return image['image'];
  }


  export function formatTimestamp (timestamp) {
    // Create a new Date object from the timestamp
    const date = new Date(timestamp);
  
    // Use toLocaleDateString with options for YYYY-MM-DD format
    return date.toLocaleDateString('en-CA'); // 'en-CA' gives the format YYYY-MM-DD
  }