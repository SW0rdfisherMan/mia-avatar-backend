import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class TechSolution:
    """Represents a technical solution with steps and requirements"""
    id: str
    title: str
    description: str
    category: str
    difficulty: str  # 'easy', 'medium', 'hard'
    estimated_time: str
    prerequisites: List[str]
    steps: List[str]
    troubleshooting_tips: List[str]
    related_issues: List[str]
    keywords: List[str]

class TechSupportKnowledge:
    """
    Comprehensive knowledge base for technical support
    Contains solutions, troubleshooting guides, and technical information
    """
    
    def __init__(self):
        self.solutions = self._load_solutions()
        self.common_issues = self._load_common_issues()
        self.quick_fixes = self._load_quick_fixes()
        self.diagnostic_questions = self._load_diagnostic_questions()
        
    def find_solution(self, query: str, category: str = None) -> List[TechSolution]:
        """
        Find relevant solutions based on user query
        """
        query_lower = query.lower()
        relevant_solutions = []
        
        for solution in self.solutions:
            # Check if query matches keywords, title, or description
            relevance_score = 0
            
            # Check keywords
            for keyword in solution.keywords:
                if keyword.lower() in query_lower:
                    relevance_score += 2
            
            # Check title
            if any(word in solution.title.lower() for word in query_lower.split()):
                relevance_score += 3
            
            # Check description
            if any(word in solution.description.lower() for word in query_lower.split()):
                relevance_score += 1
            
            # Filter by category if specified
            if category and solution.category != category:
                relevance_score = 0
            
            if relevance_score > 0:
                relevant_solutions.append((solution, relevance_score))
        
        # Sort by relevance score
        relevant_solutions.sort(key=lambda x: x[1], reverse=True)
        
        return [solution for solution, score in relevant_solutions[:5]]
    
    def get_quick_fix(self, issue_type: str) -> Optional[Dict[str, Any]]:
        """
        Get a quick fix for common issues
        """
        return self.quick_fixes.get(issue_type.lower())
    
    def get_diagnostic_questions(self, category: str) -> List[str]:
        """
        Get diagnostic questions to help identify the problem
        """
        return self.diagnostic_questions.get(category, [])
    
    def _load_solutions(self) -> List[TechSolution]:
        """Load comprehensive technical solutions"""
        solutions_data = [
            {
                'id': 'xeta_router_installation',
                'title': 'XETA Router Installation Guide',
                'description': 'Complete step-by-step installation instructions for XETA router system',
                'category': 'xeta_installation',
                'difficulty': 'medium',
                'estimated_time': '30-45 minutes',
                'prerequisites': ['XETA router kit', 'Access to ISP modem', 'Phone access to ISP if needed'],
                'steps': [
                    'If you have an all-in-one modem and WiFi Router that your ISP provided, you will need to call them and ask how to turn off the WiFi function in your existing router and also how to put your modem in "bridge mode". Once this is complete, plug in the power cable for the Xeta router and connect the ethernet port labeled with the globe icon to a free ethernet port on your ISP modem device.',
                    'If you have a separate WiFi system such as an "Eero" or "Netgear Orbi", unplug the ethernet cable from your existing WiFI device and connect it to your Xeta router using the ethernet port that has the globe icon next to it.',
                    'Once the XETA router is connected to your ISP modem and powered on, scan the QR code at the bottom of the Xeta router and follow the step-by-step instructions to configure the first XETA router.',
                    'Once the setup process is complete on the first XETA router, plug in the second XETA router in the desired location (ideally a second floor or other location to maximize coverage). Plug it in to power. On the first XETA box there is a small white button on the back of the router at the very top above the ethernet ports. Push it once. It should start blinking white. Go to the second router and push the same button once. Allow 15 min for the devices to sync.'
                ],
                'troubleshooting_tips': [
                    'Ensure the globe icon ethernet port is used for ISP connection',
                    'Wait for full 15 minutes during router sync process',
                    'Contact ISP if unsure about bridge mode configuration',
                    'Check that both routers are powered on during sync'
                ],
                'related_issues': ['xeta_network_benefits', 'xeta_earning_system'],
                'keywords': ['xeta', 'router', 'installation', 'setup', 'bridge mode', 'sync', 'ethernet', 'globe icon']
            },
            {
                'id': 'xeta_network_benefits',
                'title': 'XETA Network Security and Financial Benefits',
                'description': 'Understanding the main benefits of using the XETA Network from security and financial perspectives',
                'category': 'xeta_benefits',
                'difficulty': 'easy',
                'estimated_time': '5 minutes',
                'prerequisites': ['Interest in XETA Network'],
                'steps': [
                    'Security Benefits: With a decentralized system, hacking and criminal activity are significantly reduced on our network. Single points of failure cannot occur on a decentralized network. All of our passwords cannot be hacked at one time. If a burglar breaks into your home, they have access to your entire home. If a hacker hacks the Xeta Network, it is like breaking into a post office where they have to break into each box individually, because the data is stored in bits across the entire network instead of being housed at one place that can be hacked one time and give access to all the stored data.',
                    'Financial Benefits (Tokenomics): We at Xeta have a closed ecosystem. So, where coins on an exchange are hyped up by speculation (i.e., meme coins and ghost projects that have no actual value), Xeta coin is actually connected to the network, paying you in Xeta coin for every data transfer on the network. When deregulation came in for long-distance companies in the 1990s, Excel Telecommunications created a company that allowed you to own a piece of their network, getting paid from every phone call made on the network. Now, fast forward to the future: Xeta allows you to make money every time data is exchanged or transferred on our network.'
                ],
                'troubleshooting_tips': [
                    'Compare to traditional centralized systems to understand security advantages',
                    'Think of the Excel Telecommunications analogy for earning potential',
                    'Remember that XETA coin has real utility unlike speculative coins'
                ],
                'related_issues': ['xeta_router_installation', 'xeta_earning_system'],
                'keywords': ['xeta', 'benefits', 'security', 'decentralized', 'tokenomics', 'earning', 'network', 'hacking', 'excel telecommunications']
            },
            {
                'id': 'xeta_sales_information',
                'title': 'XETA Package Pricing and Discount Information',
                'description': 'Complete pricing information and available discounts for XETA packages',
                'category': 'xeta_sales',
                'difficulty': 'easy',
                'estimated_time': '2 minutes',
                'prerequisites': ['Interest in purchasing XETA'],
                'steps': [
                    'The XETA Starter Kit is $1,350 for the complete system',
                    'This includes 2 WiFi7 routers and access to the earning network',
                    'Use coupon code HENRYBLOUNT for a 50% discount on your XETA PACKAGE',
                    'The system pays for itself over time through earning opportunities'
                ],
                'troubleshooting_tips': [
                    'Apply the HENRYBLOUNT coupon code at checkout for maximum savings',
                    'Consider the long-term earning potential when evaluating the investment',
                    'Contact sales team for additional questions about packages'
                ],
                'related_issues': ['xeta_network_benefits', 'xeta_router_installation'],
                'keywords': ['xeta', 'price', 'cost', 'discount', 'coupon', 'henryblount', 'package', 'starter kit', 'wifi7']
            },
            {
                'id': 'wifi_connection_issues',
                'title': 'Fix WiFi Connection Problems',
                'description': 'Comprehensive guide to resolve WiFi connectivity issues',
                'category': 'network',
                'difficulty': 'easy',
                'estimated_time': '5-10 minutes',
                'prerequisites': ['Access to router', 'Device with WiFi capability'],
                'steps': [
                    'Check if WiFi is enabled on your device',
                    'Restart your WiFi adapter (disable and re-enable)',
                    'Forget and reconnect to the WiFi network',
                    'Restart your router (unplug for 30 seconds, then plug back in)',
                    'Check for interference from other devices',
                    'Update your network adapter drivers',
                    'Reset network settings if other steps fail'
                ],
                'troubleshooting_tips': [
                    'Try connecting another device to test if the issue is device-specific',
                    'Check if you\'re within range of the router',
                    'Ensure you\'re using the correct WiFi password',
                    'Try connecting to a different WiFi network to isolate the issue'
                ],
                'related_issues': ['slow_internet', 'intermittent_connection', 'dns_issues'],
                'keywords': ['wifi', 'wireless', 'internet', 'connection', 'network', 'router']
            },
            {
                'id': 'slow_computer_performance',
                'title': 'Speed Up Slow Computer Performance',
                'description': 'Steps to improve computer speed and responsiveness',
                'category': 'performance',
                'difficulty': 'medium',
                'estimated_time': '15-30 minutes',
                'prerequisites': ['Administrative access to computer'],
                'steps': [
                    'Check available disk space (should have at least 15% free)',
                    'Run disk cleanup to remove temporary files',
                    'Disable unnecessary startup programs',
                    'Update your operating system and drivers',
                    'Run antivirus scan to check for malware',
                    'Check for background processes consuming resources',
                    'Consider adding more RAM if consistently high memory usage',
                    'Defragment hard drive (for traditional HDDs only)'
                ],
                'troubleshooting_tips': [
                    'Use Task Manager to identify resource-heavy processes',
                    'Check if the slowdown occurs in specific applications',
                    'Monitor CPU and memory usage over time',
                    'Consider if the slowdown started after installing new software'
                ],
                'related_issues': ['high_cpu_usage', 'memory_issues', 'startup_problems'],
                'keywords': ['slow', 'performance', 'speed', 'lag', 'freeze', 'computer', 'laptop']
            },
            {
                'id': 'password_reset_guide',
                'title': 'Reset Forgotten Passwords Safely',
                'description': 'Secure methods to reset various types of passwords',
                'category': 'security',
                'difficulty': 'easy',
                'estimated_time': '5-15 minutes',
                'prerequisites': ['Access to recovery email or phone', 'Security questions answers'],
                'steps': [
                    'Identify the type of account (email, social media, work account, etc.)',
                    'Go to the official login page for the service',
                    'Click on "Forgot Password" or "Reset Password" link',
                    'Enter your username or email address',
                    'Choose recovery method (email, SMS, security questions)',
                    'Follow the instructions sent to your recovery method',
                    'Create a strong new password',
                    'Update password in your password manager',
                    'Enable two-factor authentication if available'
                ],
                'troubleshooting_tips': [
                    'Check spam folder for password reset emails',
                    'Ensure you\'re using the correct email address',
                    'Try different browsers if the reset page isn\'t working',
                    'Contact customer support if automated reset fails'
                ],
                'related_issues': ['account_locked', 'two_factor_issues', 'email_access'],
                'keywords': ['password', 'reset', 'forgot', 'login', 'account', 'access', 'security']
            },
            {
                'id': 'printer_not_working',
                'title': 'Fix Common Printer Problems',
                'description': 'Troubleshoot and resolve printer connectivity and printing issues',
                'category': 'hardware',
                'difficulty': 'medium',
                'estimated_time': '10-20 minutes',
                'prerequisites': ['Printer and computer', 'Printer cables or WiFi access'],
                'steps': [
                    'Check printer power and connection status',
                    'Verify printer is set as default printer',
                    'Check ink or toner levels',
                    'Clear any paper jams',
                    'Restart both printer and computer',
                    'Update or reinstall printer drivers',
                    'Run printer troubleshooter (Windows) or reset printing system (Mac)',
                    'Check print queue for stuck jobs and clear if necessary'
                ],
                'troubleshooting_tips': [
                    'Try printing a test page from printer settings',
                    'Check if other devices can print to the same printer',
                    'Ensure printer and computer are on the same network (for wireless)',
                    'Try using a different USB cable if using wired connection'
                ],
                'related_issues': ['print_quality_issues', 'scanner_problems', 'driver_issues'],
                'keywords': ['printer', 'printing', 'print', 'paper jam', 'ink', 'toner', 'driver']
            },
            {
                'id': 'email_setup_guide',
                'title': 'Set Up Email on Various Devices',
                'description': 'Configure email accounts on computers, phones, and tablets',
                'category': 'software',
                'difficulty': 'medium',
                'estimated_time': '10-15 minutes',
                'prerequisites': ['Email account credentials', 'Internet connection'],
                'steps': [
                    'Gather email account information (email, password, server settings)',
                    'Open email application or go to email settings',
                    'Choose "Add Account" or "New Account"',
                    'Select account type (IMAP, POP3, or Exchange)',
                    'Enter email address and password',
                    'Configure server settings if not auto-detected',
                    'Test sending and receiving emails',
                    'Set up additional preferences (sync frequency, signatures, etc.)'
                ],
                'troubleshooting_tips': [
                    'Use IMAP instead of POP3 for better synchronization',
                    'Check with email provider for correct server settings',
                    'Ensure two-factor authentication is properly configured',
                    'Try removing and re-adding the account if issues persist'
                ],
                'related_issues': ['sync_problems', 'authentication_errors', 'missing_emails'],
                'keywords': ['email', 'setup', 'configure', 'outlook', 'gmail', 'imap', 'pop3', 'exchange']
            },
            {
                'id': 'virus_malware_removal',
                'title': 'Remove Viruses and Malware',
                'description': 'Detect and remove malicious software from your computer',
                'category': 'security',
                'difficulty': 'medium',
                'estimated_time': '30-60 minutes',
                'prerequisites': ['Antivirus software', 'Internet connection'],
                'steps': [
                    'Disconnect from internet to prevent further damage',
                    'Boot into Safe Mode',
                    'Run full system scan with updated antivirus software',
                    'Use additional malware removal tools (Malwarebytes, etc.)',
                    'Remove or quarantine detected threats',
                    'Clear browser cache and reset browser settings',
                    'Update operating system and all software',
                    'Change all important passwords',
                    'Enable real-time protection and firewall'
                ],
                'troubleshooting_tips': [
                    'Use multiple scanning tools for thorough detection',
                    'Check for suspicious browser extensions',
                    'Monitor system performance after cleaning',
                    'Consider professional help for persistent infections'
                ],
                'related_issues': ['browser_hijacking', 'pop_up_ads', 'identity_theft'],
                'keywords': ['virus', 'malware', 'antivirus', 'security', 'infection', 'trojan', 'spyware']
            }
        ]
        
        solutions = []
        for data in solutions_data:
            solution = TechSolution(**data)
            solutions.append(solution)
        
        return solutions
    
    def _load_common_issues(self) -> Dict[str, Dict[str, Any]]:
        """Load common technical issues and their characteristics"""
        return {
            'slow_internet': {
                'symptoms': ['Pages load slowly', 'Videos buffer frequently', 'Downloads take too long'],
                'common_causes': ['Network congestion', 'ISP issues', 'Router problems', 'Too many devices'],
                'quick_checks': ['Speed test', 'Router restart', 'Check connected devices']
            },
            'computer_freeze': {
                'symptoms': ['Screen becomes unresponsive', 'Mouse/keyboard not working', 'Programs stop responding'],
                'common_causes': ['Insufficient RAM', 'Overheating', 'Software conflicts', 'Hardware issues'],
                'quick_checks': ['Force restart', 'Check running programs', 'Monitor temperature']
            },
            'blue_screen': {
                'symptoms': ['Blue screen with error message', 'Computer restarts unexpectedly', 'System crashes'],
                'common_causes': ['Driver issues', 'Hardware failure', 'Memory problems', 'System file corruption'],
                'quick_checks': ['Note error code', 'Check recent changes', 'Run memory test']
            },
            'no_sound': {
                'symptoms': ['No audio from speakers', 'Headphones not working', 'Microphone not detected'],
                'common_causes': ['Muted audio', 'Wrong output device', 'Driver issues', 'Hardware problems'],
                'quick_checks': ['Check volume settings', 'Test different audio devices', 'Update drivers']
            }
        }
    
    def _load_quick_fixes(self) -> Dict[str, Dict[str, Any]]:
        """Load quick fixes for immediate problems"""
        return {
            'internet_slow': {
                'title': 'Quick Internet Speed Fix',
                'steps': [
                    'Restart your router (unplug for 30 seconds)',
                    'Close unnecessary browser tabs and applications',
                    'Move closer to your WiFi router',
                    'Switch to 5GHz WiFi band if available'
                ],
                'estimated_time': '2-3 minutes'
            },
            'computer_slow': {
                'title': 'Quick Computer Speed Boost',
                'steps': [
                    'Close unnecessary programs and browser tabs',
                    'Restart your computer',
                    'Check available disk space',
                    'Disable startup programs you don\'t need'
                ],
                'estimated_time': '3-5 minutes'
            },
            'printer_offline': {
                'title': 'Quick Printer Fix',
                'steps': [
                    'Turn printer off and on again',
                    'Check printer connection (USB or WiFi)',
                    'Set printer as default in settings',
                    'Clear print queue of stuck jobs'
                ],
                'estimated_time': '2-4 minutes'
            },
            'email_not_syncing': {
                'title': 'Quick Email Sync Fix',
                'steps': [
                    'Check internet connection',
                    'Refresh or sync email manually',
                    'Check email account settings',
                    'Restart email application'
                ],
                'estimated_time': '1-2 minutes'
            }
        }
    
    def _load_diagnostic_questions(self) -> Dict[str, List[str]]:
        """Load diagnostic questions to help identify problems"""
        return {
            'network': [
                'Are other devices able to connect to the internet?',
                'When did you first notice the connection problem?',
                'Are you using WiFi or ethernet cable?',
                'Have you recently changed any network settings?',
                'Is the problem with all websites or specific ones?'
            ],
            'performance': [
                'When did you first notice the computer running slowly?',
                'Does the slowness occur with specific programs?',
                'How much available disk space do you have?',
                'Have you installed any new software recently?',
                'Does the computer feel hot or make unusual noises?'
            ],
            'hardware': [
                'Is the device properly connected and powered on?',
                'Are there any visible error messages or lights?',
                'When did the hardware last work properly?',
                'Have you tried different cables or connections?',
                'Is the problem consistent or intermittent?'
            ],
            'software': [
                'What error message are you seeing, if any?',
                'When did you last update the software?',
                'Does the problem occur with other similar programs?',
                'Have you tried restarting the application?',
                'Are you using the latest version of the software?'
            ],
            'security': [
                'Have you noticed any unusual computer behavior?',
                'Are you seeing unexpected pop-ups or advertisements?',
                'Have you clicked on any suspicious links recently?',
                'Is your antivirus software up to date?',
                'Have you shared your passwords with anyone?'
            ]
        }
    
    def get_solution_by_id(self, solution_id: str) -> Optional[TechSolution]:
        """Get a specific solution by its ID"""
        for solution in self.solutions:
            if solution.id == solution_id:
                return solution
        return None
    
    def get_solutions_by_category(self, category: str) -> List[TechSolution]:
        """Get all solutions in a specific category"""
        return [solution for solution in self.solutions if solution.category == category]
    
    def search_keywords(self, keywords: List[str]) -> List[TechSolution]:
        """Search solutions by multiple keywords"""
        matching_solutions = []
        
        for solution in self.solutions:
            match_count = 0
            for keyword in keywords:
                if keyword.lower() in [k.lower() for k in solution.keywords]:
                    match_count += 1
            
            if match_count > 0:
                matching_solutions.append((solution, match_count))
        
        # Sort by number of matching keywords
        matching_solutions.sort(key=lambda x: x[1], reverse=True)
        
        return [solution for solution, count in matching_solutions]
    
    def get_related_solutions(self, solution_id: str) -> List[TechSolution]:
        """Get solutions related to a specific solution"""
        solution = self.get_solution_by_id(solution_id)
        if not solution:
            return []
        
        related_solutions = []
        for related_id in solution.related_issues:
            related_solution = self.get_solution_by_id(related_id)
            if related_solution:
                related_solutions.append(related_solution)
        
        return related_solutions


    
    def get_solution(self, problem_description: str, language: str = 'english') -> Dict[str, Any]:
        """
        Get a solution for a specific problem description
        """
        problem_lower = problem_description.lower()
        
        # Map problem keywords to solution categories
        if any(keyword in problem_lower for keyword in ['wifi', 'wi-fi', 'internet', 'connection', 'network']):
            return self.get_wifi_solution(language)
        elif any(keyword in problem_lower for keyword in ['password', 'login', 'reset', 'forgot']):
            return self.get_password_solution(language)
        elif any(keyword in problem_lower for keyword in ['email', 'mail', 'outlook', 'gmail']):
            return self.get_email_solution(language)
        elif any(keyword in problem_lower for keyword in ['slow', 'performance', 'lag', 'freeze']):
            return self.get_performance_solution(language)
        elif any(keyword in problem_lower for keyword in ['printer', 'print', 'printing']):
            return self.get_printer_solution(language)
        elif any(keyword in problem_lower for keyword in ['install', 'software', 'program']):
            return self.get_installation_solution(language)
        else:
            return self.get_general_solution(language)
    
    def get_wifi_solution(self, language: str) -> Dict[str, Any]:
        """Get WiFi troubleshooting solution"""
        if language == 'spanish':
            return {
                'title': 'Solución de Problemas WiFi',
                'category': 'wifi_redes',
                'difficulty': 'básico',
                'estimated_time': '10-15 minutos',
                'steps': [
                    'Verificar que el WiFi esté habilitado en su dispositivo',
                    'Reiniciar el router desconectándolo por 30 segundos',
                    'Verificar que la contraseña de red sea correcta',
                    'Acercarse al router para mejor señal',
                    'Olvidar y reconectar a la red WiFi'
                ],
                'additional_help': 'Si el problema persiste, contacte a su proveedor de internet'
            }
        else:
            return {
                'title': 'WiFi Troubleshooting Solution',
                'category': 'wifi_networking',
                'difficulty': 'basic',
                'estimated_time': '10-15 minutes',
                'steps': [
                    'Verify WiFi is enabled on your device',
                    'Restart router by unplugging for 30 seconds',
                    'Check that network password is correct',
                    'Move closer to router for better signal',
                    'Forget and reconnect to WiFi network'
                ],
                'additional_help': 'If problem persists, contact your internet provider'
            }
    
    def get_password_solution(self, language: str) -> Dict[str, Any]:
        """Get password reset solution"""
        if language == 'spanish':
            return {
                'title': 'Restablecimiento de Contraseña',
                'category': 'contrasenas_seguridad',
                'difficulty': 'básico',
                'estimated_time': '5-10 minutos',
                'steps': [
                    'Ir a la página de inicio de sesión del servicio',
                    'Hacer clic en "¿Olvidaste tu contraseña?"',
                    'Ingresar dirección de correo electrónico',
                    'Revisar correo para enlace de restablecimiento',
                    'Crear nueva contraseña segura'
                ],
                'additional_help': 'Use contraseñas únicas para cada cuenta'
            }
        else:
            return {
                'title': 'Password Reset Solution',
                'category': 'password_security',
                'difficulty': 'basic',
                'estimated_time': '5-10 minutes',
                'steps': [
                    'Go to the service login page',
                    'Click "Forgot Password?" link',
                    'Enter your email address',
                    'Check email for reset link',
                    'Create new secure password'
                ],
                'additional_help': 'Use unique passwords for each account'
            }
    
    def get_email_solution(self, language: str) -> Dict[str, Any]:
        """Get email configuration solution"""
        if language == 'spanish':
            return {
                'title': 'Configuración de Correo',
                'category': 'configuracion_correo',
                'difficulty': 'básico',
                'estimated_time': '10-15 minutos',
                'steps': [
                    'Abrir configuración del dispositivo',
                    'Buscar configuración de Correo',
                    'Seleccionar "Agregar Cuenta"',
                    'Elegir proveedor de correo',
                    'Ingresar credenciales de correo'
                ],
                'additional_help': 'Verificar configuración del servidor si es necesario'
            }
        else:
            return {
                'title': 'Email Configuration Solution',
                'category': 'email_setup',
                'difficulty': 'basic',
                'estimated_time': '10-15 minutes',
                'steps': [
                    'Open device settings',
                    'Find Mail or Email settings',
                    'Select "Add Account"',
                    'Choose email provider',
                    'Enter email credentials'
                ],
                'additional_help': 'Check server settings if needed'
            }
    
    def get_performance_solution(self, language: str) -> Dict[str, Any]:
        """Get computer performance solution"""
        if language == 'spanish':
            return {
                'title': 'Optimización de Rendimiento',
                'category': 'problemas_hardware',
                'difficulty': 'básico',
                'estimated_time': '20-30 minutos',
                'steps': [
                    'Reiniciar la computadora',
                    'Cerrar programas innecesarios',
                    'Ejecutar limpieza de disco',
                    'Verificar espacio disponible',
                    'Actualizar sistema operativo'
                ],
                'additional_help': 'Considerar actualización de hardware si es muy antigua'
            }
        else:
            return {
                'title': 'Performance Optimization Solution',
                'category': 'hardware_issues',
                'difficulty': 'basic',
                'estimated_time': '20-30 minutes',
                'steps': [
                    'Restart your computer',
                    'Close unnecessary programs',
                    'Run disk cleanup',
                    'Check available storage space',
                    'Update operating system'
                ],
                'additional_help': 'Consider hardware upgrade if computer is very old'
            }
    
    def get_printer_solution(self, language: str) -> Dict[str, Any]:
        """Get printer troubleshooting solution"""
        if language == 'spanish':
            return {
                'title': 'Solución de Problemas de Impresora',
                'category': 'problemas_hardware',
                'difficulty': 'básico',
                'estimated_time': '15-25 minutos',
                'steps': [
                    'Verificar que la impresora esté encendida',
                    'Comprobar conexión de cables o WiFi',
                    'Verificar niveles de tinta/tóner',
                    'Revisar si hay papel cargado',
                    'Reiniciar impresora y computadora'
                ],
                'additional_help': 'Actualizar controladores de impresora si es necesario'
            }
        else:
            return {
                'title': 'Printer Troubleshooting Solution',
                'category': 'hardware_issues',
                'difficulty': 'basic',
                'estimated_time': '15-25 minutes',
                'steps': [
                    'Check that printer is powered on',
                    'Verify cable or WiFi connection',
                    'Check ink/toner levels',
                    'Ensure paper is loaded',
                    'Restart printer and computer'
                ],
                'additional_help': 'Update printer drivers if necessary'
            }
    
    def get_installation_solution(self, language: str) -> Dict[str, Any]:
        """Get software installation solution"""
        if language == 'spanish':
            return {
                'title': 'Instalación de Software',
                'category': 'instalacion_software',
                'difficulty': 'básico',
                'estimated_time': '15-30 minutos',
                'steps': [
                    'Descargar instalador del sitio oficial',
                    'Ejecutar como administrador',
                    'Seguir asistente de instalación',
                    'Aceptar términos de licencia',
                    'Reiniciar si es requerido'
                ],
                'additional_help': 'Deshabilitar antivirus temporalmente si hay problemas'
            }
        else:
            return {
                'title': 'Software Installation Solution',
                'category': 'software_installation',
                'difficulty': 'basic',
                'estimated_time': '15-30 minutes',
                'steps': [
                    'Download installer from official website',
                    'Run as administrator',
                    'Follow installation wizard',
                    'Accept license terms',
                    'Restart if required'
                ],
                'additional_help': 'Temporarily disable antivirus if issues occur'
            }
    
    def get_general_solution(self, language: str) -> Dict[str, Any]:
        """Get general troubleshooting solution"""
        if language == 'spanish':
            return {
                'title': 'Solución General de Problemas',
                'category': 'general',
                'difficulty': 'básico',
                'estimated_time': '10-20 minutos',
                'steps': [
                    'Describir el problema específico',
                    'Reiniciar el dispositivo',
                    'Verificar conexiones',
                    'Buscar actualizaciones',
                    'Contactar soporte técnico si persiste'
                ],
                'additional_help': 'Proporcionar detalles específicos ayuda a resolver más rápido'
            }
        else:
            return {
                'title': 'General Troubleshooting Solution',
                'category': 'general',
                'difficulty': 'basic',
                'estimated_time': '10-20 minutes',
                'steps': [
                    'Describe the specific problem',
                    'Restart the device',
                    'Check connections',
                    'Look for updates',
                    'Contact technical support if persists'
                ],
                'additional_help': 'Providing specific details helps resolve faster'
            }
    
    def search_faq(self, query: str, language: str = 'english') -> List[Dict[str, Any]]:
        """
        Search FAQ database for relevant questions and answers
        """
        import json
        from pathlib import Path
        
        # Load appropriate FAQ file
        if language == 'spanish':
            faq_file = Path('/home/ubuntu/mia_avatar_project/knowledge_base/faq/spanish_faq.json')
        else:
            faq_file = Path('/home/ubuntu/mia_avatar_project/knowledge_base/faq/english_faq.json')
        
        if not faq_file.exists():
            return []
        
        try:
            with open(faq_file, 'r', encoding='utf-8') as f:
                faq_data = json.load(f)
            
            results = []
            query_lower = query.lower()
            
            # Search through all categories
            for category_key, category_data in faq_data['faq_database']['categories'].items():
                for question_data in category_data['questions']:
                    # Check if query matches question, keywords, or answer
                    if (query_lower in question_data['question'].lower() or
                        query_lower in question_data['short_answer'].lower() or
                        any(keyword in query_lower for keyword in question_data['keywords'])):
                        
                        results.append({
                            'id': question_data['id'],
                            'question': question_data['question'],
                            'short_answer': question_data['short_answer'],
                            'detailed_answer': question_data['detailed_answer'],
                            'category': category_data['category_name'],
                            'difficulty': question_data['difficulty'],
                            'estimated_time': question_data['estimated_time'],
                            'keywords': question_data['keywords']
                        })
            
            # Sort by relevance (simple keyword matching score)
            def relevance_score(item):
                score = 0
                for keyword in item['keywords']:
                    if keyword in query_lower:
                        score += 1
                return score
            
            results.sort(key=relevance_score, reverse=True)
            return results[:5]  # Return top 5 results
            
        except Exception as e:
            print(f"Error searching FAQ: {e}")
            return []


    def get_xeta_solution(self, issue_type: str, language: str = "english") -> Dict[str, Any]:
        """Get XETA-specific solutions"""
        xeta_solutions = {
            "english": {
                "installation": {
                    "title": "XETA Router Installation",
                    "steps": [
                        "Determine your current setup (all-in-one modem/router or separate WiFi system)",
                        "For all-in-one: Call ISP to enable bridge mode and disable WiFi",
                        "For separate WiFi: Unplug ethernet from existing WiFi device",
                        "Connect XETA router using globe-icon ethernet port",
                        "Scan QR code on router bottom for setup",
                        "Install second router for mesh coverage",
                        "Use white sync button on both routers, wait 15 minutes"
                    ],
                    "troubleshooting": [
                        "Verify bridge mode is enabled on ISP modem",
                        "Check all ethernet connections are secure",
                        "Ensure both routers are powered on",
                        "Wait full 15 minutes for mesh sync"
                    ]
                },
                "earning": {
                    "title": "XETA Token Earning",
                    "explanation": "Earn XETA tokens by keeping your router online, sharing bandwidth, hosting data, and running AI compute tasks",
                    "requirements": [
                        "XETA Starter Kit properly installed",
                        "Stable internet connection", 
                        "Router powered on 24/7 for maximum earnings",
                        "Registered XETA account at xeta.net"
                    ]
                },
                "account_access": {
                    "title": "XETA Account Access",
                    "steps": [
                        "Go to xeta.net",
                        "Click Account > Log In",
                        "Enter email address and click Continue",
                        "Check email for verification link",
                        "Click verification link to access account"
                    ]
                }
            },
            "spanish": {
                "installation": {
                    "title": "Instalación del Router XETA",
                    "steps": [
                        "Determina tu configuración actual (módem/router todo-en-uno o sistema WiFi separado)",
                        "Para todo-en-uno: Llama al ISP para habilitar modo puente y deshabilitar WiFi",
                        "Para WiFi separado: Desconecta ethernet del dispositivo WiFi existente",
                        "Conecta router XETA usando puerto ethernet con ícono de globo",
                        "Escanea código QR en la parte inferior del router para configuración",
                        "Instala segundo router para cobertura mesh",
                        "Usa botón blanco de sincronización en ambos routers, espera 15 minutos"
                    ],
                    "troubleshooting": [
                        "Verifica que el modo puente esté habilitado en el módem ISP",
                        "Revisa que todas las conexiones ethernet estén seguras",
                        "Asegúrate de que ambos routers estén encendidos",
                        "Espera los 15 minutos completos para sincronización mesh"
                    ]
                },
                "earning": {
                    "title": "Ganar Tokens XETA",
                    "explanation": "Gana tokens XETA manteniendo tu router en línea, compartiendo ancho de banda, alojando datos y ejecutando tareas de cómputo de IA",
                    "requirements": [
                        "Kit Inicial XETA instalado correctamente",
                        "Conexión a internet estable",
                        "Router encendido 24/7 para máximas ganancias", 
                        "Cuenta XETA registrada en xeta.net"
                    ]
                },
                "account_access": {
                    "title": "Acceso a Cuenta XETA",
                    "steps": [
                        "Ve a xeta.net",
                        "Haz clic en Account > Log In",
                        "Ingresa dirección de email y haz clic en Continue",
                        "Revisa email para enlace de verificación",
                        "Haz clic en enlace de verificación para acceder a cuenta"
                    ]
                }
            }
        }
        
        return xeta_solutions.get(language, {}).get(issue_type, {
            "title": "XETA Support",
            "message": "For XETA-specific support, please contact support@xeta.net"
        })
    
    def search_xeta_faq(self, query: str, language: str = "english") -> List[Dict[str, Any]]:
        """Search XETA FAQ database"""
        # This would integrate with the XETA FAQ JSON files
        faq_keywords = {
            "english": {
                "earn": ["earn", "money", "tokens", "income", "payment"],
                "install": ["install", "setup", "router", "connection"],
                "account": ["account", "login", "access", "verification"],
                "support": ["support", "help", "contact", "troubleshooting"]
            },
            "spanish": {
                "earn": ["ganar", "dinero", "tokens", "ingresos", "pago"],
                "install": ["instalar", "configurar", "router", "conexión"],
                "account": ["cuenta", "login", "acceso", "verificación"],
                "support": ["soporte", "ayuda", "contacto", "solución"]
            }
        }
        
        # Simple keyword matching - in production would use more sophisticated search
        query_lower = query.lower()
        results = []
        
        for category, keywords in faq_keywords.get(language, {}).items():
            if any(keyword in query_lower for keyword in keywords):
                if category == "earn" and language == "english":
                    results.append({
                        "question": "How do I make money with the XETA AI KIT?",
                        "answer": "You earn XETA tokens by keeping your device online, hosting data, running compute tasks, and sharing bandwidth. The longer you're online, the more you earn.",
                        "category": "earning"
                    })
                elif category == "earn" and language == "spanish":
                    results.append({
                        "question": "¿Cómo gano dinero con el KIT de IA XETA?",
                        "answer": "Ganas tokens XETA manteniendo tu dispositivo en línea, alojando datos, ejecutando tareas de cómputo y compartiendo ancho de banda. Mientras más tiempo estés en línea, más ganas.",
                        "category": "ganar"
                    })
        
        return results[:3]  # Return top 3 results

