#!/usr/bin/env node

/**
 * Script de Otimização de Imagens - Genesys Tecnologia
 * 
 * Este script:
 * 1. Converte imagens para WebP
 * 2. Redimensiona para tamanhos adequados
 * 3. Comprime com qualidade otimizada
 * 4. Mantém originais como fallback
 * 
 * Uso: node scripts/optimize-images.js
 */

const sharp = require('sharp');
const fs = require('fs').promises;
const path = require('path');

// Configurações
const CONFIG = {
    inputDir: 'public/images',
    outputDir: 'public/images/optimized',
    backupDir: 'public/images/originals',

    // Tamanhos máximos
    sizes: {
        logo: { width: 512, height: 512 },
        photo: { width: 800, height: 800 },
        banner: { width: 1920, height: 1080 },
    },

    // Qualidades
    quality: {
        webp: 85,
        jpeg: 85,
        png: 90,
    },
};

// Cores para console
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    red: '\x1b[31m',
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

// Determina o tipo de imagem pelo nome
function getImageType(filename) {
    const lower = filename.toLowerCase();
    if (lower.includes('logo')) return 'logo';
    if (lower.includes('banner') || lower.includes('hero')) return 'banner';
    return 'photo';
}

// Otimiza uma imagem
async function optimizeImage(inputPath, filename) {
    try {
        const type = getImageType(filename);
        const size = CONFIG.sizes[type];
        const ext = path.extname(filename).toLowerCase();
        const basename = path.basename(filename, ext);

        log(`\n📸 Processando: ${filename}`, 'blue');

        // Ler metadados da imagem
        const metadata = await sharp(inputPath).metadata();
        log(`   Tamanho original: ${metadata.width}x${metadata.height} (${(metadata.size / 1024).toFixed(2)} KB)`, 'yellow');

        // Criar pipeline de otimização
        let pipeline = sharp(inputPath);

        // Redimensionar se necessário
        if (metadata.width > size.width || metadata.height > size.height) {
            pipeline = pipeline.resize(size.width, size.height, {
                fit: 'inside',
                withoutEnlargement: true,
            });
            log(`   ✓ Redimensionado para max ${size.width}x${size.height}`, 'green');
        }

        // Converter para WebP
        const webpPath = path.join(CONFIG.outputDir, `${basename}.webp`);
        await pipeline
            .clone()
            .webp({ quality: CONFIG.quality.webp })
            .toFile(webpPath);

        const webpStats = await fs.stat(webpPath);
        log(`   ✓ WebP criado: ${(webpStats.size / 1024).toFixed(2)} KB`, 'green');

        // Manter fallback no formato original
        let fallbackPath;
        if (ext === '.png') {
            fallbackPath = path.join(CONFIG.outputDir, `${basename}.png`);
            await pipeline
                .clone()
                .png({ quality: CONFIG.quality.png, compressionLevel: 9 })
                .toFile(fallbackPath);
        } else {
            fallbackPath = path.join(CONFIG.outputDir, `${basename}.jpg`);
            await pipeline
                .clone()
                .jpeg({ quality: CONFIG.quality.jpeg, progressive: true })
                .toFile(fallbackPath);
        }

        const fallbackStats = await fs.stat(fallbackPath);
        log(`   ✓ Fallback criado: ${(fallbackStats.size / 1024).toFixed(2)} KB`, 'green');

        // Calcular economia
        const originalSize = metadata.size;
        const optimizedSize = webpStats.size;
        const savings = ((originalSize - optimizedSize) / originalSize * 100).toFixed(1);
        log(`   💰 Economia: ${savings}%`, 'green');

        return {
            original: filename,
            originalSize,
            optimizedSize,
            savings: parseFloat(savings),
        };

    } catch (error) {
        log(`   ❌ Erro ao processar ${filename}: ${error.message}`, 'red');
        return null;
    }
}

// Função principal
async function main() {
    try {
        log('\n🖼️  Iniciando Otimização de Imagens...', 'blue');
        log('='.repeat(50), 'blue');

        // Criar diretórios
        await fs.mkdir(CONFIG.outputDir, { recursive: true });
        await fs.mkdir(CONFIG.backupDir, { recursive: true });
        log('\n✓ Diretórios criados', 'green');

        // Listar imagens
        const files = await fs.readdir(CONFIG.inputDir);
        const imageFiles = files.filter(f => /\.(jpg|jpeg|png)$/i.test(f));

        log(`\n📁 Encontradas ${imageFiles.length} imagens para otimizar`, 'yellow');

        // Processar cada imagem
        const results = [];
        for (const file of imageFiles) {
            const inputPath = path.join(CONFIG.inputDir, file);
            const result = await optimizeImage(inputPath, file);
            if (result) results.push(result);

            // Fazer backup do original
            const backupPath = path.join(CONFIG.backupDir, file);
            await fs.copyFile(inputPath, backupPath);
        }

        // Resumo
        log('\n' + '='.repeat(50), 'blue');
        log('📊 RESUMO DA OTIMIZAÇÃO', 'blue');
        log('='.repeat(50), 'blue');

        const totalOriginal = results.reduce((sum, r) => sum + r.originalSize, 0);
        const totalOptimized = results.reduce((sum, r) => sum + r.optimizedSize, 0);
        const totalSavings = ((totalOriginal - totalOptimized) / totalOriginal * 100).toFixed(1);

        log(`\n✓ Imagens processadas: ${results.length}`, 'green');
        log(`✓ Tamanho original: ${(totalOriginal / 1024 / 1024).toFixed(2)} MB`, 'yellow');
        log(`✓ Tamanho otimizado: ${(totalOptimized / 1024 / 1024).toFixed(2)} MB`, 'green');
        log(`✓ Economia total: ${totalSavings}% (${((totalOriginal - totalOptimized) / 1024 / 1024).toFixed(2)} MB)`, 'green');

        log('\n📁 Arquivos salvos em:', 'blue');
        log(`   - Otimizados: ${CONFIG.outputDir}`, 'yellow');
        log(`   - Originais (backup): ${CONFIG.backupDir}`, 'yellow');

        log('\n✅ Otimização concluída com sucesso!', 'green');
        log('\n💡 Próximos passos:', 'blue');
        log('   1. Revisar imagens otimizadas', 'yellow');
        log('   2. Substituir imagens originais pelas otimizadas', 'yellow');
        log('   3. Testar no navegador', 'yellow');
        log('   4. Fazer commit das mudanças\n', 'yellow');

    } catch (error) {
        log(`\n❌ Erro fatal: ${error.message}`, 'red');
        process.exit(1);
    }
}

// Executar
if (require.main === module) {
    main();
}

module.exports = { optimizeImage };
