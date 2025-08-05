# 🤝 コントリビューションガイド

日本語会議記録文字起こしアプリへの貢献をありがとうございます！

## 🚀 貢献方法

### バグ報告

バグを見つけた場合：

1. [Issues](https://github.com/yourusername/mojiokoshi/issues)で既存の報告を確認
2. 新しいIssueを作成し、以下を含める：
   - 発生環境（OS、Pythonバージョン）
   - 再現手順
   - 期待される動作
   - 実際の動作
   - エラーメッセージ（あれば）

### 機能要望

新機能のアイデアがある場合：

1. [Issues](https://github.com/yourusername/mojiokoshi/issues)で提案
2. 以下を含める：
   - 機能の説明
   - 使用ケース
   - 実装案（あれば）

### プルリクエスト

コードの改善を提案する場合：

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 🛠️ 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/mojiokoshi.git
cd mojiokoshi

# 開発用の依存関係をインストール
pip install -r requirements.txt
pip install pytest black flake8

# pre-commitフックをセットアップ
pip install pre-commit
pre-commit install
```

## 📝 コーディング規約

### Python

- [PEP 8](https://pep8.org/)に従う
- Black でフォーマット: `black .`
- Flake8 でリント: `flake8 .`
- 型ヒントを使用
- docstringを適切に記述

### コミットメッセージ

```
type(scope): description

詳細な説明（必要に応じて）

Fixes #issue_number
```

**Type:**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント更新
- `style`: コードスタイル修正
- `refactor`: リファクタリング
- `test`: テスト追加・修正
- `chore`: その他の変更

## 🧪 テスト

新しい機能やバグ修正には必ずテストを追加：

```bash
# テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=modules

# 特定のテストファイル
pytest tests/test_audio_processor.py
```

## 📚 ドキュメント

- READMEの更新
- API変更時はdocstringの更新
- 新機能には使用例を追加

## 🎯 優先度の高い貢献分野

1. **音声認識精度の向上**
   - 新しいプロンプトテンプレートの提案
   - 専門分野特化の後処理ロジック

2. **新しいLLMプロバイダーの追加**
   - Claude、Cohere、その他のAPIサポート

3. **UI/UX改善**
   - Web UIの追加
   - GUI版の開発

4. **パフォーマンス最適化**
   - 並列処理の改善
   - メモリ使用量の最適化

5. **多言語対応**
   - 英語、韓国語、中国語等のサポート

## 💡 開発のヒント

### 新しいLLMプロバイダーの追加

1. `modules/llm_processor.py`に新しいクライアントクラスを追加
2. `LLMProcessor`クラスに統合
3. 設定ファイルにAPI情報を追加
4. テストを追加

### 新しい出力フォーマットの追加

1. `modules/output_formatter.py`に新しいフォーマット関数を追加
2. CLIオプションに追加
3. テストを追加

## 🤔 質問・相談

- 開発に関する質問は[Discussions](https://github.com/yourusername/mojiokoshi/discussions)で
- Discordサーバー: [招待リンク](https://discord.gg/mojiokoshi)

## 📄 ライセンス

コントリビューションは[MIT License](LICENSE)の下で提供されます。

---

貢献してくださる皆様、ありがとうございます！ 🙏