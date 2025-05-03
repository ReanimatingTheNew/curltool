// 网站多语言翻译文件
const translations = {
    // 英文翻译
    'en': {
        // 元数据
        'meta_title': 'Curl to JSON Tool | Convert curl commands online',
        'meta_description': 'Convert curl commands to structured JSON format with our tool. Supports complex parameter parsing and provides a clean interface for developers to analyze HTTP requests.',
        'meta_keywords': 'curl to json,curl command parser,API debugging tool,HTTP request analysis',
        
        // 社交媒体标签
        'og_title': 'Curl to JSON Tool | Convert curl commands to JSON format online',
        'og_description': 'Quickly convert curl commands to structured JSON format, supporting various complex parameter parsing. Provides a clean web interface and API.',
        'twitter_title': 'Curl to JSON Tool | Convert curl commands to JSON format online',
        'twitter_description': 'Quickly convert curl commands to structured JSON format, supporting various complex parameter parsing. Provides a clean web interface and API.',
        
        // 页面标题和描述
        'site_title': 'Curl to JSON Tool',
        'site_description': 'Convert curl commands to JSON format for quick analysis and processing of HTTP requests',
        
        // 导航菜单
        'nav_tool': 'Online Converter',
        'nav_api': 'API Docs',
        'nav_examples': 'Examples',
        'nav_about': 'About',
        
        // 内容目录
        'toc_title': 'Table of Contents',
        'toc_tool': 'Online Converter',
        'toc_api': 'API Documentation',
        'toc_api_endpoint': 'Endpoint',
        'toc_request_format': 'Request Format',
        'toc_response_format': 'Response Format',
        'toc_examples': 'Examples',
        'toc_about': 'About',
        
        // 转换工具区域
        'tool_title': 'Online Converter',
        'tool_description': 'Paste your curl command in the input box below, click the "Convert" button to get structured JSON format. Supports various complex curl parameters and options.',
        'input_title': 'Enter curl command',
        'input_placeholder': 'Paste your curl command here, for example: curl -X POST https://api.example.com -H \'Content-Type: application/json\' -d \'{\"key\":\"value\"}\'',
        'btn_convert': 'Convert',
        'btn_clear': 'Clear',
        'output_title': 'JSON Result',
        'btn_copy': 'Copy',
        'btn_format': 'Format',
        'output_placeholder': '// Conversion result will be displayed here',
        
        // API区域
        'api_title': 'API Documentation',
        'api_description': 'This tool provides a simple and easy-to-use API interface that can be integrated into your application for automated curl command parsing and conversion.',
        'api_endpoint_title': 'Endpoint',
        'api_endpoint_desc': 'Use the following HTTP request method and path to access the API:',
        'request_format_title': 'Request Format',
        'request_format_desc': 'The request body should be in JSON format, containing a `curl` field with the curl command string to be parsed:',
        'response_format_title': 'Response Format',
        'response_format_desc': 'The response content is a structured JSON object containing the following fields:',
        'response_method': 'HTTP request method',
        'response_url': 'Request URL',
        'response_headers': 'Request headers',
        'response_data': 'Request data',
        
        // 示例代码区域
        'examples_title': 'Example Code',
        'examples_description': 'Here are examples of calling this tool\'s API in different programming languages:',
        
        // 关于工具部分
        'about_title': 'About Curl to JSON Tool',
        'about_description': 'Curl to JSON Tool is an online utility designed specifically for developers, aimed at simplifying API debugging and HTTP request analysis. By converting complex curl commands into structured JSON format, developers can more easily understand and process HTTP requests.',
        'features_title': 'Key Features',
        'feature_1': 'Fast Conversion - Convert curl commands to JSON format instantly',
        'feature_2': 'Comprehensive Parsing - Support for various curl parameters such as request methods, headers, data, etc.',
        'feature_3': 'API Interface - Provides a simple and easy-to-use API for integration with other systems',
        'feature_4': 'User Friendly - Intuitive interface design and interaction experience',
        'use_cases_title': 'Use Cases',
        'use_case_1': 'API Development and Testing',
        'use_case_2': 'Network Request Debugging',
        'use_case_3': 'Automation Script Writing',
        'use_case_4': 'Learning HTTP Protocol',
        
        // 页脚
        'footer_nav_title': 'Quick Navigation',
        'footer_copyright': '© 2025 Curl to JSON Tool | A simple and efficient API debugging tool',
        'footer_description': 'This tool is designed to help developers handle HTTP requests more efficiently, improving development and debugging productivity.',
        
        // 语言切换
        'language_switch': 'Language',
        'lang_en': 'English',
        'lang_zh': '中文'
    },
    
    // 中文翻译
    'zh': {
        // 元数据
        'meta_title': 'Curl转JSON工具 | 在线转换curl命令',
        'meta_description': '使用我们的工具将curl命令转换为结构化JSON格式。支持复杂参数解析，并为开发者提供清晰的界面分析HTTP请求。',
        'meta_keywords': 'curl转json,curl命令解析,API调试工具,HTTP请求分析',
        
        // 社交媒体标签
        'og_title': 'Curl转JSON工具 | 在线快速转换curl命令为JSON格式',
        'og_description': '快速将curl命令转换为结构化JSON格式，支持各种复杂参数解析。提供简洁的Web界面和API接口。',
        'twitter_title': 'Curl转JSON工具 | 在线快速转换curl命令为JSON格式',
        'twitter_description': '快速将curl命令转换为结构化JSON格式，支持各种复杂参数解析。提供简洁的Web界面和API接口。',
        
        // 页面标题和描述
        'site_title': 'Curl转JSON工具',
        'site_description': '将curl命令转换为JSON格式，便于开发者快速分析和处理HTTP请求',
        
        // 导航菜单
        'nav_tool': '在线转换工具',
        'nav_api': 'API文档',
        'nav_examples': '使用示例',
        'nav_about': '关于工具',
        
        // 内容目录
        'toc_title': '内容目录',
        'toc_tool': '在线转换工具',
        'toc_api': 'API使用说明',
        'toc_api_endpoint': '接口地址',
        'toc_request_format': '请求格式',
        'toc_response_format': '响应格式',
        'toc_examples': '使用示例',
        'toc_about': '关于工具',
        
        // 转换工具区域
        'tool_title': '在线转换工具',
        'tool_description': '在下面的输入框中粘贴您的curl命令，点击"转换"按钮即可获得结构化的JSON格式。支持各种复杂的curl参数和选项。',
        'input_title': '输入curl命令',
        'input_placeholder': '在这里粘贴您的curl命令，例如：curl -X POST https://api.example.com -H \'Content-Type: application/json\' -d \'{\"key\":\"value\"}\'',
        'btn_convert': '转换',
        'btn_clear': '清除',
        'output_title': 'JSON结果',
        'btn_copy': '复制',
        'btn_format': '格式化',
        'output_placeholder': '// 转换结果将显示在这里',
        
        // API区域
        'api_title': 'API使用说明',
        'api_description': '本工具提供了简单易用的API接口，可以集成到您的应用程序中，实现自动化的curl命令解析和转换。',
        'api_endpoint_title': '接口地址',
        'api_endpoint_desc': '使用以下HTTP请求方法和路径访问接口：',
        'request_format_title': '请求格式',
        'request_format_desc': '请求体应为JSON格式，包含一个`curl`字段，值为要解析的curl命令字符串：',
        'response_format_title': '响应格式',
        'response_format_desc': '响应内容为结构化的JSON对象，包含以下字段：',
        'response_method': 'HTTP请求方法',
        'response_url': '请求URL',
        'response_headers': '请求头信息',
        'response_data': '请求数据',
        
        // 示例代码区域
        'examples_title': '示例代码',
        'examples_description': '以下是不同编程语言中调用本工具API的示例代码：',
        
        // 关于工具部分
        'about_title': '关于Curl转JSON工具',
        'about_description': 'Curl转JSON工具是一个专为开发者设计的在线实用工具，旨在简化API调试和HTTP请求分析过程。通过将复杂的curl命令转换为结构化的JSON格式，开发者可以更轻松地理解和处理HTTP请求。',
        'features_title': '主要功能',
        'feature_1': '快速转换 - 将curl命令即时转换为JSON格式',
        'feature_2': '全面解析 - 支持多种curl参数，如请求方法、头信息、数据等',
        'feature_3': 'API接口 - 提供简单易用的API，便于集成到其他系统',
        'feature_4': '用户友好 - 直观的界面设计和交互体验',
        'use_cases_title': '适用场景',
        'use_case_1': 'API开发和测试',
        'use_case_2': '网络请求调试',
        'use_case_3': '自动化脚本编写',
        'use_case_4': '学习HTTP协议',
        
        // 页脚
        'footer_nav_title': '快速导航',
        'footer_copyright': '© 2025 Curl转JSON工具 | 一个简单高效的API调试工具',
        'footer_description': '本工具旨在帮助开发者更高效地处理HTTP请求，提升开发和调试效率。',
        
        // 语言切换
        'language_switch': '语言',
        'lang_en': 'English',
        'lang_zh': '中文',
        'lang_hi': 'हिन्दी',
        'lang_fr': 'Français',
        'lang_de': 'Deutsch',
        'lang_es': 'Español'
    },
    
    // 印地语翻译
    'hi': {
        // 元数据
        'meta_title': 'Curl से JSON टूल | ऑनलाइन curl कमांड कनवर्टर',
        'meta_description': 'हमारे टूल से curl कमांड को JSON प्रारूप में बदलें। जटिल पैरामीटर पार्सिंग का समर्थन करता है और डेवलपर्स को HTTP अनुरोधों के विश्लेषण के लिए साफ इंटरफेस प्रदान करता है।',
        'meta_keywords': 'curl से json,curl कमांड पार्सर,API डीबगिंग टूल,HTTP अनुरोध विश्लेषण',
        
        // 社交媒体标签
        'og_title': 'Curl से JSON टूल | ऑनलाइन curl कमांड को JSON प्रारूप में बदलें',
        'og_description': 'जल्दी से curl कमांड को संरचित JSON प्रारूप में बदलें, विभिन्न जटिल पैरामीटर पार्सिंग का समर्थन करें। एक साफ वेब इंटरफेस और API प्रदान करता है।',
        'twitter_title': 'Curl से JSON टूल | ऑनलाइन curl कमांड को JSON प्रारूप में बदलें',
        'twitter_description': 'जल्दी से curl कमांड को संरचित JSON प्रारूप में बदलें, विभिन्न जटिल पैरामीटर पार्सिंग का समर्थन करें। एक साफ वेब इंटरफेस और API प्रदान करता है।',
        
        // 页面标题和描述
        'site_title': 'Curl से JSON टूल',
        'site_description': 'HTTP अनुरोधों के त्वरित विश्लेषण और प्रसंस्करण के लिए curl कमांड को JSON प्रारूप में बदलें',
        
        // 导航菜单
        'nav_tool': 'ऑनलाइन कन्वर्टर',
        'nav_api': 'API दस्तावेज़',
        'nav_examples': 'उदाहरण',
        'nav_about': 'परिचय',
        
        // 内容目录
        'toc_title': 'विषय-सूची',
        'toc_tool': 'ऑनलाइन कन्वर्टर',
        'toc_api': 'API दस्तावेज़ीकरण',
        'toc_api_endpoint': 'एंडपॉइंट',
        'toc_request_format': 'अनुरोध प्रारूप',
        'toc_response_format': 'प्रतिक्रिया प्रारूप',
        'toc_examples': 'उदाहरण',
        'toc_about': 'परिचय',
        
        // 转换工具区域
        'tool_title': 'ऑनलाइन कन्वर्टर',
        'tool_description': 'अपने curl कमांड को नीचे दिए गए इनपुट बॉक्स में पेस्ट करें, संरचित JSON प्रारूप प्राप्त करने के लिए "कन्वर्ट" बटन पर क्लिक करें। विभिन्न जटिल curl पैरामीटर और विकल्पों का समर्थन करता है।',
        'input_title': 'curl कमांड दर्ज करें',
'input_placeholder': 'अपना curl कमांड यहां पेस्ट करें, उदाहरण के लिए: curl -X POST https://api.example.com -H \'Content-Type: application/json\' -d \'{"key":"value"}\'',
        'btn_convert': 'कन्वर्ट',
        'btn_clear': 'साफ़ करें',
        'output_title': 'JSON परिणाम',
        'btn_copy': 'कॉपी',
        'btn_format': 'फॉर्मेट',
        'output_placeholder': '// रूपांतरण परिणाम यहां प्रदर्शित किया जाएगा',
        
        // API区域
        'api_title': 'API दस्तावेज़ीकरण',
        'api_description': 'यह टूल एक सरल और उपयोग में आसान API इंटरफेस प्रदान करता है जिसे स्वचालित curl कमांड पार्सिंग और रूपांतरण के लिए आपके एप्लिकेशन में एकीकृत किया जा सकता है।',
        'api_endpoint_title': 'एंडपॉइंट',
        'api_endpoint_desc': 'API तक पहुंचने के लिए निम्न HTTP अनुरोध विधि और पथ का उपयोग करें:',
        'request_format_title': 'अनुरोध प्रारूप',
        'request_format_desc': 'अनुरोध बॉडी JSON प्रारूप में होनी चाहिए, जिसमें पार्स किए जाने वाले curl कमांड स्ट्रिंग के साथ एक `curl` फील्ड हो:',
        'response_format_title': 'प्रतिक्रिया प्रारूप',
        'response_format_desc': 'प्रतिक्रिया सामग्री एक संरचित JSON ऑब्जेक्ट है जिसमें निम्न फील्ड्स शामिल हैं:',
        'response_method': 'HTTP अनुरोध विधि',
        'response_url': 'अनुरोध URL',
        'response_headers': 'अनुरोध हेडर्स',
        'response_data': 'अनुरोध डेटा',
        
        // 示例代码区域
        'examples_title': 'उदाहरण कोड',
        'examples_description': 'विभिन्न प्रोग्रामिंग भाषाओं में इस टूल के API को कॉल करने के उदाहरण यहां दिए गए हैं:',
        
        // 关于工具部分
        'about_title': 'Curl से JSON टूल के बारे में',
        'about_description': 'Curl से JSON टूल विशेष रूप से डेवलपर्स के लिए डिज़ाइन किया गया एक ऑनलाइन उपयोगिता है, जिसका उद्देश्य API डीबगिंग और HTTP अनुरोध विश्लेषण को सरल बनाना है। जटिल curl कमांड को संरचित JSON प्रारूप में बदलकर, डेवलपर्स आसानी से HTTP अनुरोधों को समझ और संसाधित कर सकते हैं।',
        'features_title': 'मुख्य विशेषताएं',
        'feature_1': 'तेज़ रूपांतरण - curl कमांड को तुरंत JSON प्रारूप में बदलें',
        'feature_2': 'व्यापक पार्सिंग - अनुरोध विधियों, हेडर्स, डेटा आदि जैसे विभिन्न curl पैरामीटर के लिए समर्थन',
        'feature_3': 'API इंटरफेस - अन्य सिस्टम के साथ एकीकरण के लिए एक सरल और उपयोग में आसान API प्रदान करता है',
        'feature_4': 'उपयोगकर्ता अनुकूल - सहज इंटरफेस डिज़ाइन और इंटरैक्शन अनुभव',
        'use_cases_title': 'उपयोग के मामले',
        'use_case_1': 'API विकास और परीक्षण',
        'use_case_2': 'नेटवर्क अनुरोध डीबगिंग',
        'use_case_3': 'स्वचालन स्क्रिप्ट लेखन',
        'use_case_4': 'HTTP प्रोटोकॉल सीखना',
        
        // 页脚
        'footer_nav_title': 'त्वरित नेविगेशन',
        'footer_copyright': '© 2025 Curl से JSON टूल | एक सरल और कुशल API डीबगिंग टूल',
        'footer_description': 'यह टूल डेवलपर्स को HTTP अनुरोधों को अधिक कुशलता से संभालने में मदद करने के लिए डिज़ाइन किया गया है, जिससे विकास और डीबगिंग उत्पादकता में सुधार होता है।',
        
        // 语言切换
        'language_switch': 'भाषा',
        'lang_en': 'English',
        'lang_zh': '中文',
        'lang_hi': 'हिन्दी',
        'lang_fr': 'Français',
        'lang_de': 'Deutsch',
        'lang_es': 'Español'
    },
    
    // 法语翻译
    'fr': {
        // 元数据
        'meta_title': 'Outil Curl vers JSON | Convertisseur de commandes curl',
        'meta_description': 'Convertissez les commandes curl en format JSON structuré avec notre outil. Supporte l\'analyse de paramètres complexes et offre une interface claire pour analyser les requêtes HTTP.',
        'meta_keywords': 'curl vers json,analyseur de commandes curl,outil de débogage API,analyse de requêtes HTTP',
        
        // 社交媒体标签
        'og_title': 'Outil Curl vers JSON | Convertir les commandes curl en format JSON en ligne',
        'og_description': 'Convertissez rapidement les commandes curl en format JSON structuré, prenant en charge diverses analyses de paramètres complexes. Fournit une interface web claire et une API.',
        'twitter_title': 'Outil Curl vers JSON | Convertir les commandes curl en format JSON en ligne',
        'twitter_description': 'Convertissez rapidement les commandes curl en format JSON structuré, prenant en charge diverses analyses de paramètres complexes. Fournit une interface web claire et une API.',
        
        // 页面标题和描述
        'site_title': 'Outil Curl vers JSON',
        'site_description': 'Convertir les commandes curl en format JSON pour une analyse et un traitement rapides des requêtes HTTP',
        
        // 导航菜单
        'nav_tool': 'Convertisseur en ligne',
        'nav_api': 'Documentation API',
        'nav_examples': 'Exemples',
        'nav_about': 'À propos',
        
        // 内容目录
        'toc_title': 'Table des matières',
        'toc_tool': 'Convertisseur en ligne',
        'toc_api': 'Documentation API',
        'toc_api_endpoint': 'Point de terminaison',
        'toc_request_format': 'Format de requête',
        'toc_response_format': 'Format de réponse',
        'toc_examples': 'Exemples',
        'toc_about': 'À propos',
        
        // 转换工具区域
        'tool_title': 'Convertisseur en ligne',
        'tool_description': 'Collez votre commande curl dans la zone de saisie ci-dessous, cliquez sur le bouton "Convertir" pour obtenir un format JSON structuré. Prend en charge divers paramètres et options curl complexes.',
        'input_title': 'Entrez la commande curl',
        'input_placeholder': 'Collez votre commande curl ici, par exemple: curl -X POST https://api.example.com -H \'Content-Type: application/json\' -d \'{"key":"value"}\'\'',
        'btn_convert': 'Convertir',
        'btn_clear': 'Effacer',
        'output_title': 'Résultat JSON',
        'btn_copy': 'Copier',
        'btn_format': 'Formater',
        'output_placeholder': '// Le résultat de la conversion sera affiché ici',
        
        // API区域
        'api_title': 'Documentation API',
        'api_description': 'Cet outil fournit une interface API simple et facile à utiliser qui peut être intégrée à votre application pour l\'analyse et la conversion automatisées des commandes curl.',
        'api_endpoint_title': 'Point de terminaison',
        'api_endpoint_desc': 'Utilisez la méthode et le chemin de requête HTTP suivants pour accéder à l\'API:',
        'request_format_title': 'Format de requête',
        'request_format_desc': 'Le corps de la requête doit être au format JSON, contenant un champ `curl` avec la chaîne de commande curl à analyser:',
        'response_format_title': 'Format de réponse',
        'response_format_desc': 'Le contenu de la réponse est un objet JSON structuré contenant les champs suivants:',
        'response_method': 'Méthode de requête HTTP',
        'response_url': 'URL de requête',
        'response_headers': 'En-têtes de requête',
        'response_data': 'Données de requête',
        
        // 示例代码区域
        'examples_title': 'Exemples de code',
        'examples_description': 'Voici des exemples d\'appel de l\'API de cet outil dans différents langages de programmation:',
        
        // 关于工具部分
        'about_title': 'À propos de l\'outil Curl vers JSON',
        'about_description': 'L\'outil Curl vers JSON est un utilitaire en ligne conçu spécifiquement pour les développeurs, visant à simplifier le débogage des API et l\'analyse des requêtes HTTP. En convertissant les commandes curl complexes en format JSON structuré, les développeurs peuvent plus facilement comprendre et traiter les requêtes HTTP.',
        'features_title': 'Fonctionnalités principales',
        'feature_1': 'Conversion rapide - Convertir instantanément les commandes curl en format JSON',
        'feature_2': 'Analyse complète - Prise en charge de divers paramètres curl tels que les méthodes de requête, les en-têtes, les données, etc.',
        'feature_3': 'Interface API - Fournit une API simple et facile à utiliser pour l\'intégration avec d\'autres systèmes',
        'feature_4': 'Convivial - Conception d\'interface intuitive et expérience d\'interaction',
        'use_cases_title': 'Cas d\'utilisation',
        'use_case_1': 'Développement et test d\'API',
        'use_case_2': 'Débogage de requêtes réseau',
        'use_case_3': 'Rédaction de scripts d\'automatisation',
        'use_case_4': 'Apprentissage du protocole HTTP',
        
        // 页脚
        'footer_nav_title': 'Navigation rapide',
        'footer_copyright': '© 2025 Outil Curl vers JSON | Un outil de débogage API simple et efficace',
        'footer_description': 'Cet outil est conçu pour aider les développeurs à gérer plus efficacement les requêtes HTTP, améliorant la productivité de développement et de débogage.',
        
        // 语言切换
        'language_switch': 'Langue',
        'lang_en': 'English',
        'lang_zh': '中文',
        'lang_hi': 'हिन्दी',
        'lang_fr': 'Français',
        'lang_de': 'Deutsch',
        'lang_es': 'Español'
    },
    
    // 德语翻译
    'de': {
        // 元数据
        'meta_title': 'Curl zu JSON Tool | Online Curl-Befehle konvertieren',
        'meta_description': 'Konvertieren Sie Curl-Befehle in strukturiertes JSON-Format mit unserem Tool. Unterstützt komplexes Parameter-Parsing und bietet eine klare Oberfläche für HTTP-Anfragen-Analyse.',
        'meta_keywords': 'curl zu json,curl-befehl-parser,API-debugging-tool,HTTP-anfragen-analyse',
        
        // 社交媒体标签
        'og_title': 'Curl zu JSON Tool | Curl-Befehle online in JSON-Format konvertieren',
        'og_description': 'Konvertieren Sie Curl-Befehle schnell in strukturiertes JSON-Format, mit Unterstützung für verschiedene komplexe Parameter-Parsing. Bietet eine übersichtliche Weboberfläche und API.',
        'twitter_title': 'Curl zu JSON Tool | Curl-Befehle online in JSON-Format konvertieren',
        'twitter_description': 'Konvertieren Sie Curl-Befehle schnell in strukturiertes JSON-Format, mit Unterstützung für verschiedene komplexe Parameter-Parsing. Bietet eine übersichtliche Weboberfläche und API.',
        
        // 页面标题和描述
        'site_title': 'Curl zu JSON Tool',
        'site_description': 'Konvertieren Sie Curl-Befehle in JSON-Format für schnelle Analyse und Verarbeitung von HTTP-Anfragen',
        
        // 导航菜单
        'nav_tool': 'Online-Konverter',
        'nav_api': 'API-Dokumentation',
        'nav_examples': 'Beispiele',
        'nav_about': 'Über',
        
        // 内容目录
        'toc_title': 'Inhaltsverzeichnis',
        'toc_tool': 'Online-Konverter',
        'toc_api': 'API-Dokumentation',
        'toc_api_endpoint': 'Endpunkt',
        'toc_request_format': 'Anforderungsformat',
        'toc_response_format': 'Antwortformat',
        'toc_examples': 'Beispiele',
        'toc_about': 'Über',
        
        // 转换工具区域
        'tool_title': 'Online-Konverter',
        'tool_description': 'Fügen Sie Ihren Curl-Befehl in das Eingabefeld unten ein, klicken Sie auf die Schaltfläche "Konvertieren", um ein strukturiertes JSON-Format zu erhalten. Unterstützt verschiedene komplexe Curl-Parameter und Optionen.',
        'input_title': 'Curl-Befehl eingeben',
        'input_placeholder': 'Fügen Sie Ihren Curl-Befehl hier ein, zum Beispiel: curl -X POST https://api.example.com -H \'Content-Type: application/json\' -d \'{"key":"value"}\'\'',
        'btn_convert': 'Konvertieren',
        'btn_clear': 'Löschen',
        'output_title': 'JSON-Ergebnis',
        'btn_copy': 'Kopieren',
        'btn_format': 'Formatieren',
        'output_placeholder': '// Das Konvertierungsergebnis wird hier angezeigt',
        
        // API区域
        'api_title': 'API-Dokumentation',
        'api_description': 'Dieses Tool bietet eine einfach zu bedienende API-Schnittstelle, die in Ihre Anwendung integriert werden kann, um Curl-Befehle automatisch zu analysieren und zu konvertieren.',
        'api_endpoint_title': 'Endpunkt',
        'api_endpoint_desc': 'Verwenden Sie die folgende HTTP-Anforderungsmethode und den Pfad, um auf die API zuzugreifen:',
        'request_format_title': 'Anforderungsformat',
        'request_format_desc': 'Der Anforderungskörper sollte im JSON-Format sein und ein `curl`-Feld mit der zu analysierenden Curl-Befehlszeichenfolge enthalten:',
        'response_format_title': 'Antwortformat',
        'response_format_desc': 'Der Antwortinhalt ist ein strukturiertes JSON-Objekt, das die folgenden Felder enthält:',
        'response_method': 'HTTP-Anforderungsmethode',
        'response_url': 'Anforderungs-URL',
        'response_headers': 'Anforderungsheader',
        'response_data': 'Anforderungsdaten',
        
        // 示例代码区域
        'examples_title': 'Beispielcode',
        'examples_description': 'Hier sind Beispiele für den Aufruf der API dieses Tools in verschiedenen Programmiersprachen:',
        
        // 关于工具部分
        'about_title': 'Über das Curl zu JSON Tool',
        'about_description': 'Das Curl zu JSON Tool ist ein Online-Dienstprogramm, das speziell für Entwickler entwickelt wurde und darauf abzielt, das Debugging von APIs und die Analyse von HTTP-Anfragen zu vereinfachen. Durch die Konvertierung komplexer Curl-Befehle in ein strukturiertes JSON-Format können Entwickler HTTP-Anfragen leichter verstehen und verarbeiten.',
        'features_title': 'Hauptfunktionen',
        'feature_1': 'Schnelle Konvertierung - Curl-Befehle sofort in JSON-Format konvertieren',
        'feature_2': 'Umfassende Analyse - Unterstützung für verschiedene Curl-Parameter wie Anforderungsmethoden, Header, Daten usw.',
        'feature_3': 'API-Schnittstelle - Bietet eine einfach zu bedienende API für die Integration mit anderen Systemen',
        'feature_4': 'Benutzerfreundlich - Intuitive Oberflächengestaltung und Interaktionserfahrung',
        'use_cases_title': 'Anwendungsfälle',
        'use_case_1': 'API-Entwicklung und -Tests',
        'use_case_2': 'Debugging von Netzwerkanfragen',
        'use_case_3': 'Schreiben von Automatisierungsskripten',
        'use_case_4': 'Erlernen des HTTP-Protokolls',
        
        // 页脚
        'footer_nav_title': 'Schnellnavigation',
        'footer_copyright': '© 2025 Curl zu JSON Tool | Ein einfaches und effizientes API-Debugging-Tool',
        'footer_description': 'Dieses Tool wurde entwickelt, um Entwicklern zu helfen, HTTP-Anfragen effizienter zu verarbeiten und die Entwicklungs- und Debugging-Produktivität zu verbessern.',
        
        // 语言切换
        'language_switch': 'Sprache',
        'lang_en': 'English',
        'lang_zh': '中文',
        'lang_hi': 'हिन्दी',
        'lang_fr': 'Français',
        'lang_de': 'Deutsch',
        'lang_es': 'Español'
    },
    
    // 西班牙语翻译
    'es': {
        // 元数据
        'meta_title': 'Herramienta Curl a JSON | Convertidor de comandos curl',
        'meta_description': 'Convierta comandos curl a formato JSON estructurado con nuestra herramienta. Admite análisis de parámetros complejos y ofrece una interfaz clara para analizar solicitudes HTTP.',
        'meta_keywords': 'curl a json,analizador de comandos curl,herramienta de depuración de API,análisis de solicitudes HTTP',
        
        // 社交媒体标签
        'og_title': 'Herramienta Curl a JSON | Convertir comandos curl a formato JSON en línea',
        'og_description': 'Convierte rápidamente comandos curl a formato JSON estructurado, admitiendo diversos análisis de parámetros complejos. Proporciona una interfaz web limpia y una API.',
        'twitter_title': 'Herramienta Curl a JSON | Convertir comandos curl a formato JSON en línea',
        'twitter_description': 'Convierte rápidamente comandos curl a formato JSON estructurado, admitiendo diversos análisis de parámetros complejos. Proporciona una interfaz web limpia y una API.',
        
        // 页面标题和描述
        'site_title': 'Herramienta Curl a JSON',
        'site_description': 'Convierte comandos curl a formato JSON para un análisis y procesamiento rápido de solicitudes HTTP',
        
        // 导航菜单
        'nav_tool': 'Convertidor en línea',
        'nav_api': 'Documentación API',
        'nav_examples': 'Ejemplos',
        'nav_about': 'Acerca de',
        
        // 内容目录
        'toc_title': 'Tabla de contenidos',
        'toc_tool': 'Convertidor en línea',
        'toc_api': 'Documentación API',
        'toc_api_endpoint': 'Punto final',
        'toc_request_format': 'Formato de solicitud',
        'toc_response_format': 'Formato de respuesta',
        'toc_examples': 'Ejemplos',
        'toc_about': 'Acerca de',
        
        // 转换工具区域
        'tool_title': 'Convertidor en línea',
        'tool_description': 'Pegue su comando curl en el cuadro de entrada a continuación, haga clic en el botón "Convertir" para obtener un formato JSON estructurado. Admite varios parámetros y opciones curl complejos.',
        'input_title': 'Ingrese el comando curl',
        'input_placeholder': 'Pegue su comando curl aquí, por ejemplo: curl -X POST https://api.example.com -H \'Content-Type: application/json\' -d \'{"key":"value"}\'\'',
        'btn_convert': 'Convertir',
        'btn_clear': 'Limpiar',
        'output_title': 'Resultado JSON',
        'btn_copy': 'Copiar',
        'btn_format': 'Formatear',
        'output_placeholder': '// El resultado de la conversión se mostrará aquí',
        
        // API区域
        'api_title': 'Documentación API',
        'api_description': 'Esta herramienta proporciona una interfaz API simple y fácil de usar que se puede integrar en su aplicación para el análisis y la conversión automatizados de comandos curl.',
        'api_endpoint_title': 'Punto final',
        'api_endpoint_desc': 'Utilice el siguiente método y ruta de solicitud HTTP para acceder a la API:',
        'request_format_title': 'Formato de solicitud',
        'request_format_desc': 'El cuerpo de la solicitud debe estar en formato JSON, conteniendo un campo `curl` con la cadena de comando curl a analizar:',
        'response_format_title': 'Formato de respuesta',
        'response_format_desc': 'El contenido de la respuesta es un objeto JSON estructurado que contiene los siguientes campos:',
        'response_method': 'Método de solicitud HTTP',
        'response_url': 'URL de solicitud',
        'response_headers': 'Encabezados de solicitud',
        'response_data': 'Datos de solicitud',
        
        // 示例代码区域
        'examples_title': 'Código de ejemplo',
        'examples_description': 'Aquí hay ejemplos de cómo llamar a la API de esta herramienta en diferentes lenguajes de programación:',
        
        // 关于工具部分
        'about_title': 'Acerca de la herramienta Curl a JSON',
        'about_description': 'La herramienta Curl a JSON es una utilidad en línea diseñada específicamente para desarrolladores, con el objetivo de simplificar la depuración de API y el análisis de solicitudes HTTP. Al convertir comandos curl complejos en formato JSON estructurado, los desarrolladores pueden entender y procesar más fácilmente las solicitudes HTTP.',
        'features_title': 'Características principales',
        'feature_1': 'Conversión rápida - Convierte comandos curl a formato JSON al instante',
        'feature_2': 'Análisis completo - Soporte para varios parámetros curl como métodos de solicitud, encabezados, datos, etc.',
        'feature_3': 'Interfaz API - Proporciona una API simple y fácil de usar para la integración con otros sistemas',
        'feature_4': 'Fácil de usar - Diseño de interfaz intuitivo y experiencia de interacción',
        'use_cases_title': 'Casos de uso',
        'use_case_1': 'Desarrollo y prueba de API',
        'use_case_2': 'Depuración de solicitudes de red',
        'use_case_3': 'Escritura de scripts de automatización',
        'use_case_4': 'Aprendizaje del protocolo HTTP',
        
        // 页脚
        'footer_nav_title': 'Navegación rápida',
        'footer_copyright': '© 2025 Herramienta Curl a JSON | Una herramienta de depuración de API simple y eficiente',
        'footer_description': 'Esta herramienta está diseñada para ayudar a los desarrolladores a manejar las solicitudes HTTP de manera más eficiente, mejorando la productividad de desarrollo y depuración.',
        
        // 语言切换
        'language_switch': 'Idioma',
        'lang_en': 'English',
        'lang_zh': '中文',
        'lang_hi': 'हिन्दी',
        'lang_fr': 'Français',
        'lang_de': 'Deutsch',
        'lang_es': 'Español'
    }
};
