import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Ottica Censuales</h3>
            <p className="text-gray-400">
              La tua ottica di fiducia da oltre 30 anni. Qualità, professionalità e innovazione al servizio della tua vista.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Link Utili</h3>
            <div className="space-y-2">
              <Link href="/chi-siamo" className="block text-gray-400 hover:text-white">Chi Siamo</Link>
              <Link href="/servizi" className="block text-gray-400 hover:text-white">I Nostri Servizi</Link>
              <Link href="/negozi" className="block text-gray-400 hover:text-white">Trova il Negozio</Link>
              <Link href="/contatti" className="block text-gray-400 hover:text-white">Contatti</Link>
            </div>
          </div>

          {/* Customer Service */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Assistenza</h3>
            <div className="space-y-2">
              <Link href="/faq" className="block text-gray-400 hover:text-white">FAQ</Link>
              <Link href="/spedizioni" className="block text-gray-400 hover:text-white">Spedizioni</Link>
              <Link href="/resi" className="block text-gray-400 hover:text-white">Resi e Rimborsi</Link>
              <Link href="/privacy" className="block text-gray-400 hover:text-white">Privacy Policy</Link>
            </div>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Contattaci</h3>
            <div className="space-y-2 text-gray-400">
              <p>📞 +39 02 1234567</p>
              <p>✉️ info@otticacensuales.it</p>
              <p>🕒 Lun-Sab 9:00-19:00</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 Ottica Censuales. Tutti i diritti riservati.</p>
        </div>
      </div>
    </footer>
  )
}