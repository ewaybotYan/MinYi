# this-class-is-not-key-value-coding-compliant-for-the-key-view


今天照着书本学习iOS过程遇到一个问题，记录如下。

## 问题产生的原因

由于书籍里面的内容和最新的XCode内容有点差别，在XCode新建的 **single application view** 里面，默认有一个 **Launch Screen File** 和一个 **Storyboard** 文件，而在书本里面将的例子里面只有一个XIB文件。

为了保持统一，我就删掉了Launch Screen和Storyboard文件，自行添加了一个XIB文件，同时在 **TARGETS->Main Interface** 设置为该XIB文件(之前我一直这样干)。

这样，一运行就报错:

```
this class is not key value coding-compliant for the key view.
```

自己查了点资料，有说是 **File's Owner** 的 **Custom Class** 设置不对的，又说绑定的 **Outlet** 不对的，反正各种情况都尝试了还是不解决问题。

## 问题的解决

http://stackoverflow.com/questions/10152872/this-class-is-not-key-value-coding-compliant-for-the-key-view

**@Joseph DeCarlo**:

```
If you have a control in your nib (xib file) that is linked to a property (IBOutlet) or method (IBAction) in your view controller, and you have either deleted or renamed the property or method, the runtime can't find it because it has been renamed and therefore crashes.

In your case, you have set the Main Interface property of the project to your ViewController.nib. This is a problem because the only nibs that should be used as Main Interface should have UIWindows in them and the File Owner in that nib should be set to the AppDelegate. The UIWindow in the nib should be linked to the File Owner's (AppDelegate) window property. Because you set that with a nib without the traits the runtime was looking for, it gives you this error.

The solution is to leave the Main Interface blank as you do not have to set up UIWindows manually anymore.
```

将Main Interface的设置留空就不存在这个问题了，一个小问题花费了我不少时间，一直摸不着头脑.


## 资料

- http://stackoverflow.com/questions/10152872/this-class-is-not-key-value-coding-compliant-for-the-key-view/
