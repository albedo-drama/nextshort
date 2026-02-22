export default async function handler(req, res) {
    // Tangkap URL target yang dikirim dari index.html
    const targetUrl = req.query.url;
    
    if (!targetUrl) {
        return res.status(400).json({ error: 'URL tidak ditemukan' });
    }

    try {
        // Lakukan fetch dari server Vercel (bukan dari browser)
        const response = await fetch(targetUrl, {
            method: 'GET',
            headers: {
                // User-Agent otomatis di-inject di sini agar lolos blokir API
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            }
        });

        // Parse datanya dan kirim balik ke index.html
        const data = await response.json();
        res.status(200).json(data);
    } catch (error) {
        res.status(500).json({ status: false, error: error.message });
    }
}
