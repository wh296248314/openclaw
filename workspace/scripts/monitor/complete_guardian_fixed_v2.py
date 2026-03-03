                time.sleep(60)
                print("\n" + guardian.get_dashboard())
                
        except KeyboardInterrupt:
            print("\n🛑 收到停止信号...")
        finally:
            guardian.stop()

if __name__ == "__main__":
    main()