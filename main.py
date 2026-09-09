import json
import os
import random
import sys

class HSKManager:
    def __init__(self, filepath="data/hsk_vocab.json"):
        self.filepath = filepath
        self.vocab = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.vocab = json.load(f)
                print(f"โหลดข้อมูลคำศัพท์สำเร็จจำนวน {len(self.vocab)} คำ\n")
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}\n")
                self.vocab = []
        else:
            print(f"ไม่พบไฟล์ {self.filepath}\n")
            self.vocab = []

    def display_words(self, word_list):
        if not word_list:
            print("\nไม่พบข้อมูลคำศัพท์\n")
            return
        print("-" * 75)
        print(f"{'ID':<4} | {'HSK':<4} | {'คำศัพท์':<8} | {'พินอิน':<12} | {'ประเภท':<6} | {'คำแปล'}")
        print("-" * 75)
        for item in word_list:
            item_id = item.get("id", 0)
            level = item.get("hsk_level", "-")
            word = item.get("word", "")
            pinyin = item.get("pinyin", "")
            w_type = item.get("type", "")
            meaning = item.get("meaning", "")
            print(f"{item_id:<4} | {level:<4} | {word:<8} | {pinyin:<12} | {w_type:<6} | {meaning}")
        print("-" * 75 + "\n")

    def search(self, keyword):
        keyword = keyword.strip().lower()
        results = [
            item for item in self.vocab
            if keyword in item.get("word", "").lower()
            or keyword in item.get("pinyin", "").lower()
            or keyword in item.get("meaning", "").lower()
        ]
        return results

    def filter_level(self, level):
        return [item for item in self.vocab if item.get("hsk_level") == level]

    def start_quiz(self):
        print("\n--- ระบบแบบทดสอบคำศัพท์ ---")
        print("1. ทดสอบคำศัพท์รวมทั้งหมด")
        print("2. ทดสอบเฉพาะระดับ HSK")
        choice = input("เลือกรูปแบบการทดสอบ (1-2): ").strip()

        pool = self.vocab
        if choice == "2":
            try:
                level = int(input("ระบุระดับ HSK (1-3): ").strip())
                pool = self.filter_level(level)
            except ValueError:
                print("ระดับ HSK ไม่ถูกต้อง\n")
                return

        if not pool:
            print("ไม่มีคำศัพท์ในระบบสำหรับจัดแบบทดสอบ\n")
            return

        try:
            num_q = int(input(f"จำนวนข้อที่ต้องการทดสอบ (สูงสุด {len(pool)} ข้อ): ").strip())
            num_q = max(1, min(num_q, len(pool)))
        except ValueError:
            num_q = min(5, len(pool))

        selected = random.sample(pool, num_q)
        score = 0

        print(f"\n================ เริ่มทดสอบ ({num_q} ข้อ) ================")
        for idx, item in enumerate(selected, 1):
            print(f"\nข้อที่ {idx}/{num_q}: {item.get('word')} ({item.get('pinyin')}) [{item.get('type')}]")
            user_ans = input("คำแปลภาษาไทยคืออะไร?: ").strip()
            correct_meaning = item.get("meaning", "")

            if user_ans and (user_ans in correct_meaning or correct_meaning in user_ans):
                print("✨ ถูกต้อง!")
                score += 1
            else:
                print(f"❌ ไม่ถูกต้อง! เฉลยคือ: {correct_meaning}")
                if item.get("example"):
                    print(f"   ตัวอย่างประโยค: {item.get('example')}")

        print("\n================ สรุปผลการทดสอบ ================")
        print(f"คะแนนที่ได้: {score} / {num_q} คะแนน ({int((score / num_q) * 100)}%)")
        print("=================================================\n")

    def run(self):
        while True:
            print("================ HSK Vocabulary Manager ================")
            print("1. แสดงคำศัพท์ทั้งหมด")
            print("2. ค้นหาคำศัพท์ (ภาษาจีน / พินอิน / คำแปล)")
            print("3. กรองคำศัพท์ตามระดับ HSK")
            print("4. เริ่มแบบทดสอบคำศัพท์")
            print("5. ออกจากโปรแกรม")
            print("========================================================")
            choice = input("กรุณาเลือกรายการ (1-5): ").strip()

            if choice == "1":
                self.display_words(self.vocab)
            elif choice == "2":
                kw = input("กรอกคำที่ต้องการค้นหา: ")
                results = self.search(kw)
                self.display_words(results)
            elif choice == "3":
                try:
                    lvl = int(input("ระบุระดับ HSK (1-3): "))
                    results = self.filter_level(lvl)
                    self.display_words(results)
                except ValueError:
                    print("ข้อผิดพลาด: กรุณากรอกตัวเลขระดับ HSK\n")
            elif choice == "4":
                self.start_quiz()
            elif choice == "5":
                print("ปิดโปรแกรมเรียบร้อยแล้ว")
                sys.exit(0)
            else:
                print("ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง\n")

if __name__ == "__main__":
    app = HSKManager()
    app.run()
