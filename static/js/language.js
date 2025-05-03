// 语言切换功能
document.addEventListener('DOMContentLoaded', function() {
    // 默认语言为英语
    let currentLang = localStorage.getItem('preferred_language') || 'en';
    
    // 初始化页面语言
    setLanguage(currentLang);
    
    // 监听语言切换事件
    document.getElementById('language-selector').addEventListener('change', function(e) {
        const lang = e.target.value;
        setLanguage(lang);
        localStorage.setItem('preferred_language', lang);
    });
    
    // 设置语言选择器的初始值
    document.getElementById('language-selector').value = currentLang;
});

// 设置页面语言
function setLanguage(lang) {
    // 更新HTML lang属性
    document.documentElement.lang = lang;
    
    // 更新页面上所有带有data-i18n属性的元素
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            // 对于普通元素，更新内容
            element.textContent = translations[lang][key];
        }
    });
    
    // 更新表单元素的placeholder和value
    const placeholders = document.querySelectorAll('[data-i18n-placeholder]');
    placeholders.forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[lang] && translations[lang][key]) {
            element.placeholder = translations[lang][key];
        }
    });
    
    // 更新按钮的value属性
    const buttons = document.querySelectorAll('button[data-i18n]');
    buttons.forEach(button => {
        const key = button.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            button.textContent = translations[lang][key];
        }
    });
    
    // 更新meta标签
    updateMetaTags(lang);
}

// 更新meta标签和SEO相关信息
function updateMetaTags(lang) {
    // 更新标题
    document.title = translations[lang]['meta_title'];
    
    // 更新meta描述
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
        metaDescription.content = translations[lang]['meta_description'];
    }
    
    // 更新meta关键词
    const metaKeywords = document.querySelector('meta[name="keywords"]');
    if (metaKeywords) {
        metaKeywords.content = translations[lang]['meta_keywords'];
    }
    
    // 更新Open Graph标签
    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle) {
        ogTitle.content = translations[lang]['og_title'];
    }
    
    const ogDescription = document.querySelector('meta[property="og:description"]');
    if (ogDescription) {
        ogDescription.content = translations[lang]['og_description'];
    }
    
    // 更新Twitter Card标签
    const twitterTitle = document.querySelector('meta[name="twitter:title"]');
    if (twitterTitle) {
        twitterTitle.content = translations[lang]['twitter_title'];
    }
    
    const twitterDescription = document.querySelector('meta[name="twitter:description"]');
    if (twitterDescription) {
        twitterDescription.content = translations[lang]['twitter_description'];
    }
}
