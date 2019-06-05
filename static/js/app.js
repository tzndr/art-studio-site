
var ViewModel = function() {
  var self = this;

  this.artNightText = ko.observable("Join me on Wednesday, June 26 at Sepia Chapel, Two Rivers, from 6-8:30pm for ALCOHOL INK WASHER JEWELRY!  Who doesn't like to repurpose things?  We have worked with alcohol inks before and this one is different because we are going small and on metal!  You will be creating seven washers, and a few littles for earrings too if you'd like.  It's fun to stack em for a different look.  You are the artists and as usual, color choices and designs are all up to you.  I will walk you through step by step!  Alcohol ink is one of the most unpredictable mediums to work with.  It is SO MUCH FUN!  I will teach you a few different techniques to get different results.  It can become addicting as the layers of ink pile on.  Just think, you will be able to wear your own artwork!  Wire, cording and ear wires will be available too so you will learn a few jewelry techniques as well.  No experience is necessary!  Enjoy a complimentary glass of wine as you create!  $35  Register below!");

  this.artNightDate = ko.observable("Wednesday, June 26th 8:00PM - 9:30PM");

  this.artNightLocation = ko.observable("Sepia Chapel 1820 Jefferson St Two Rivers, WI");

  this.aboutAmyNavImg = ko.observable("../static/img/studio/about_me_thumbnail.png");

  this.artNightNavImg = ko.observable("../static/img/studio/art_night_thumbnail.png");

  this.shopNavImg = ko.observable("../static/img/studio/shop_thumbnail.png");

  this.privateEventNavImg = ko.observable("../static/img/studio/private_event_thumbnail.png");

  this.blogNavImg = ko.observable("../static/img/studio/blog_thumbnail.png");

  this.contactNavImg = ko.observable("../static/img/studio/contact_thumbnail.png");

  this.artNightDateText1 = ko.observable("Wednesday, July 24th 2019");

  this.artNightDateText2 = ko.observable("Wednesday, August 21st 2019");

  this.artNightDateText3 = ko.observable("Wednesday, August 25th 2019");

  this.resetNavImgs = function() {
    if (self.aboutAmyNavImg() != "../static/img/studio/about_me_thumbnail.png") {
      self.aboutAmyNavImg("../static/img/studio/about_me_thumbnail.png");
    }
    else if (self.artNightNavImg() != "../static/img/studio/art_night_thumbnail.png") {
      self.artNightNavImg("../static/img/studio/art_night_thumbnail.png");
    }
    else if (self.shopNavImg() != "../static/img/studio/shop_thumbnail.png") {
      self.shopNavImg("../static/img/studio/shop_thumbnail.png");
    }
    else if (self.privateEventNavImg() != "../static/img/studio/private_event_thumbnail.png") {
      self.privateEventNavImg("../static/img/studio/private_event_thumbnail.png");
    }
    else if (self.blogNavImg() != "../static/img/studio/blog_thumbnail.png") {
      self.blogNavImg("../static/img/studio/blog_thumbnail.png");
    }
    else if (self.contactNavImg() != "../static/img/studio/contact_thumbnail.png") {
      self.contactNavImg("../static/img/studio/contact_thumbnail.png");
    }
  }

  this.changeSrcAttrAboutAmy = function() {
    self.resetNavImgs();
    self.aboutAmyNavImg("../static/img/studio/about_me_thumbnail_selected.png");
    return true;
  }

  this.changeSrcAttrArtNight = function() {
    self.resetNavImgs();
    self.artNightNavImg("../static/img/studio/art_night_thumbnail_selected.png");
    return true;
  }

  this.changeSrcAttrShop = function() {
    self.resetNavImgs();
    self.shopNavImg("../static/img/studio/shop_thumbnail_selected.png");
    return true;
  }

  this.changeSrcAttrPrivateEvent = function() {
    self.resetNavImgs();
    self.privateEventNavImg("../static/img/studio/private_event_thumbnail_selected.png");
    return true;
  }

  this.changeSrcAttrBlog = function() {
    self.resetNavImgs();
    self.blogNavImg("../static/img/studio/blog_thumbnail_selected.png");
    return true;
  }

  this.changeSrcAttrContact = function() {
    self.resetNavImgs();
    self.contactNavImg("../static/img/studio/contact_thumbnail_selected.png");
    return true;
  }
}

ko.applyBindings(new ViewModel());
